"""Parser voor uren uit Obsidian dagnotities.

Verwacht formaat in dagnotities (onder een configuurbare header):

    ## Uren
    - ProjectNaam: 8u
    - AnderProject: 4 uur
    - NogEen: 2.5h

De projectnaam moet overeenkomen met een project in e-boekhouden.nl.
"""

import re
from datetime import date
from pathlib import Path


def parse_week_hours(
    obsidian_config: dict, days: list[date]
) -> dict[date, list[dict]]:
    """Parse uren uit Obsidian dagnotities voor de opgegeven dagen.

    Returns:
        Dict van datum -> lijst van {project, hours, comment} entries.
    """
    vault_path = Path(obsidian_config["vault_path"]).expanduser()
    pattern_template = obsidian_config.get(
        "daily_notes_pattern", "Daily Notes/{date}.md"
    )
    date_format = obsidian_config.get("date_format", "%Y-%m-%d")
    hours_section = obsidian_config.get("hours_section", "## Uren")
    hours_pattern = obsidian_config.get(
        "hours_pattern",
        r"^- (?P<project>.+?):\s*(?P<hours>[\d.,]+)\s*(?:u|uur|h|hours?)\s*$",
    )

    regex = re.compile(hours_pattern, re.MULTILINE)
    result = {}

    for day in days:
        date_str = day.strftime(date_format)
        note_path = vault_path / pattern_template.format(date=date_str)

        if not note_path.exists():
            continue

        content = note_path.read_text(encoding="utf-8")
        entries = _extract_hours_from_note(content, hours_section, regex)
        if entries:
            result[day] = entries

    return result


def _extract_hours_from_note(
    content: str, section_header: str, pattern: re.Pattern
) -> list[dict]:
    """Extraheer uren uit een Obsidian notitie.

    Zoekt naar de sectie met de opgegeven header en parsed
    alle regels die aan het patroon voldoen.
    """
    # Zoek de sectie
    lines = content.split("\n")
    in_section = False
    section_lines = []

    for line in lines:
        if line.strip() == section_header:
            in_section = True
            continue
        if in_section:
            # Stop bij de volgende header
            if line.startswith("#"):
                break
            section_lines.append(line)

    section_text = "\n".join(section_lines)
    entries = []

    for match in pattern.finditer(section_text):
        hours_str = match.group("hours").replace(",", ".")
        try:
            hours = float(hours_str)
        except ValueError:
            continue

        entries.append(
            {
                "project": match.group("project").strip(),
                "hours": hours,
            }
        )

    return entries
