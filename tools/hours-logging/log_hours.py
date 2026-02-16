#!/usr/bin/env python3
"""CLI tool voor het automatisch invullen van uren in e-boekhouden.nl.

Gebruik:
    python log_hours.py week              # Vul de huidige week in (ma-do, 8u)
    python log_hours.py week --date 2026-02-09  # Vul een specifieke week in
    python log_hours.py day 2026-02-16    # Vul een specifieke dag in
    python log_hours.py projects          # Toon beschikbare projecten
    python log_hours.py activities        # Toon beschikbare activiteiten
    python log_hours.py status            # Toon uren van deze maand
    python log_hours.py obsidian          # Vul uren in vanuit Obsidian notities
"""

import sys
from datetime import date, timedelta
from pathlib import Path

import click
import yaml

from eboekhouden_client import EboekhoudenClient, LoginError


def load_config() -> dict:
    config_path = Path(__file__).parent / "config.yaml"
    if not config_path.exists():
        click.echo(
            "Fout: config.yaml niet gevonden.\n"
            "Kopieer config.example.yaml naar config.yaml en vul je gegevens in:\n"
            "  cp config.example.yaml config.yaml",
            err=True,
        )
        sys.exit(1)

    with open(config_path) as f:
        return yaml.safe_load(f)


def get_client(config: dict) -> EboekhoudenClient:
    eb = config["eboekhouden"]
    try:
        return EboekhoudenClient(eb["email"], eb["password"])
    except LoginError as e:
        click.echo(f"Fout: {e}", err=True)
        sys.exit(1)


def get_week_dates(reference_date: date, workdays: list[int]) -> list[date]:
    """Bereken de werkdagen van de week waarin reference_date valt."""
    # Vind maandag van de week
    monday = reference_date - timedelta(days=reference_date.weekday())
    return [monday + timedelta(days=d) for d in workdays]


@click.group()
def cli():
    """Automatische urenregistratie voor e-boekhouden.nl."""
    pass


@cli.command()
@click.option(
    "--date", "ref_date", type=click.DateTime(formats=["%Y-%m-%d"]), default=None,
    help="Datum in de gewenste week (standaard: vandaag).",
)
@click.option("--dry-run", is_flag=True, help="Toon wat er zou worden ingevoerd zonder daadwerkelijk in te vullen.")
def week(ref_date, dry_run):
    """Vul uren in voor een hele werkweek."""
    config = load_config()
    defaults = config.get("defaults", {})

    ref = ref_date.date() if ref_date else date.today()
    workdays = defaults.get("workdays", [0, 1, 2, 3])
    hours = defaults.get("hours_per_day", 8)
    comment = defaults.get("comment", "")

    days = get_week_dates(ref, workdays)
    day_names = ["ma", "di", "wo", "do", "vr", "za", "zo"]

    click.echo(f"Week van {days[0].strftime('%d-%m-%Y')} t/m {days[-1].strftime('%d-%m-%Y')}")
    click.echo(f"  Uren per dag: {hours}")
    click.echo(f"  Werkdagen: {', '.join(day_names[d] for d in workdays)}")
    click.echo()

    if dry_run:
        for day in days:
            click.echo(f"  [DRY RUN] {day.strftime('%d-%m-%Y')} ({day_names[day.weekday()]}) - {hours}u")
        click.echo(f"\nTotaal: {hours * len(days)}u (niet ingevoerd)")
        return

    client = get_client(config)

    project_id = defaults.get("project_id") or client.get_default_project_id()
    activity_id = defaults.get("activity_id") or client.get_default_activity_id()

    if not project_id:
        click.echo("Fout: Geen project geconfigureerd. Gebruik 'projects' om beschikbare projecten te zien.", err=True)
        sys.exit(1)
    if not activity_id:
        click.echo("Fout: Geen activiteit geconfigureerd. Gebruik 'activities' om beschikbare activiteiten te zien.", err=True)
        sys.exit(1)

    for day in days:
        client.add_hours(hours, day, project_id, activity_id, comment)
        click.echo(f"  {day.strftime('%d-%m-%Y')} ({day_names[day.weekday()]}) - {hours}u")

    click.echo(f"\nTotaal: {hours * len(days)}u ingevoerd.")


@cli.command()
@click.argument("target_date", type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option("--hours", type=float, default=None, help="Aantal uren (standaard uit config).")
@click.option("--comment", default=None, help="Opmerking.")
@click.option("--dry-run", is_flag=True, help="Toon wat er zou worden ingevoerd.")
def day(target_date, hours, comment, dry_run):
    """Vul uren in voor een specifieke dag."""
    config = load_config()
    defaults = config.get("defaults", {})

    target = target_date.date()
    hours = hours or defaults.get("hours_per_day", 8)
    comment = comment if comment is not None else defaults.get("comment", "")

    if dry_run:
        click.echo(f"[DRY RUN] {target.strftime('%d-%m-%Y')} - {hours}u")
        return

    client = get_client(config)
    project_id = defaults.get("project_id") or client.get_default_project_id()
    activity_id = defaults.get("activity_id") or client.get_default_activity_id()

    if not project_id or not activity_id:
        click.echo("Fout: Project of activiteit niet geconfigureerd.", err=True)
        sys.exit(1)

    client.add_hours(hours, target, project_id, activity_id, comment)
    click.echo(f"{target.strftime('%d-%m-%Y')} - {hours}u ingevoerd.")


@cli.command()
def projects():
    """Toon beschikbare projecten."""
    config = load_config()
    client = get_client(config)

    click.echo("Beschikbare projecten:\n")
    click.echo(f"  {'ID':<10} {'Naam':<40} {'Standaard'}")
    click.echo(f"  {'─' * 10} {'─' * 40} {'─' * 10}")
    for p in client.get_projects():
        marker = "  ✓" if p["selected"] else ""
        click.echo(f"  {p['id']:<10} {p['name']:<40} {marker}")


@cli.command()
def activities():
    """Toon beschikbare activiteiten."""
    config = load_config()
    client = get_client(config)

    click.echo("Beschikbare activiteiten:\n")
    click.echo(f"  {'ID':<10} {'Naam':<40} {'Standaard'}")
    click.echo(f"  {'─' * 10} {'─' * 40} {'─' * 10}")
    for a in client.get_activities():
        marker = "  ✓" if a["selected"] else ""
        click.echo(f"  {a['id']:<10} {a['name']:<40} {marker}")


@cli.command()
def status():
    """Toon geregistreerde uren van deze maand."""
    config = load_config()
    client = get_client(config)

    entries = client.get_hours()
    if not entries:
        click.echo("Geen uren gevonden voor deze maand.")
        return

    click.echo("Uren deze maand:\n")
    for entry in entries:
        click.echo(f"  {' | '.join(entry['cells'])}")


@cli.command()
@click.option(
    "--date", "ref_date", type=click.DateTime(formats=["%Y-%m-%d"]), default=None,
    help="Datum in de gewenste week (standaard: vandaag).",
)
@click.option("--dry-run", is_flag=True, help="Toon wat er zou worden ingevoerd.")
def obsidian(ref_date, dry_run):
    """Vul uren in vanuit Obsidian dagnotities."""
    config = load_config()
    obs_config = config.get("obsidian", {})

    if not obs_config.get("vault_path"):
        click.echo(
            "Fout: Obsidian vault pad niet geconfigureerd in config.yaml.\n"
            "Stel obsidian.vault_path in.",
            err=True,
        )
        sys.exit(1)

    from obsidian_parser import parse_week_hours

    defaults = config.get("defaults", {})
    ref = ref_date.date() if ref_date else date.today()
    workdays = defaults.get("workdays", [0, 1, 2, 3])
    days = get_week_dates(ref, workdays)

    week_hours = parse_week_hours(obs_config, days)
    if not week_hours:
        click.echo("Geen uren gevonden in Obsidian notities voor deze week.")
        return

    if dry_run:
        total = 0
        for day, entries in sorted(week_hours.items()):
            for entry in entries:
                click.echo(
                    f"  [DRY RUN] {day.strftime('%d-%m-%Y')} - "
                    f"{entry['project']}: {entry['hours']}u"
                )
                total += entry["hours"]
        click.echo(f"\nTotaal: {total}u (niet ingevoerd)")
        return

    client = get_client(config)
    project_map = {p["name"].lower(): p["id"] for p in client.get_projects()}
    activity_id = defaults.get("activity_id") or client.get_default_activity_id()

    total = 0
    for day_date, entries in sorted(week_hours.items()):
        for entry in entries:
            project_name = entry["project"].lower()
            project_id = project_map.get(project_name)
            if not project_id:
                click.echo(
                    f"  Waarschuwing: Project '{entry['project']}' niet gevonden, "
                    f"overgeslagen.",
                    err=True,
                )
                continue

            client.add_hours(
                entry["hours"], day_date, project_id, activity_id, entry.get("comment", "")
            )
            click.echo(
                f"  {day_date.strftime('%d-%m-%Y')} - "
                f"{entry['project']}: {entry['hours']}u"
            )
            total += entry["hours"]

    click.echo(f"\nTotaal: {total}u ingevoerd vanuit Obsidian.")


if __name__ == "__main__":
    cli()
