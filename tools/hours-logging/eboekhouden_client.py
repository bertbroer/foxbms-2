"""Client voor e-boekhouden.nl urenregistratie via web interface."""

import re
from datetime import date

import requests
from bs4 import BeautifulSoup


class LoginError(Exception):
    """Inloggen mislukt."""


class EboekhoudenClient:
    """Web client voor e-boekhouden.nl urenregistratie.

    Gebruikt HTTP sessies en form submissions (geen SOAP/REST API
    beschikbaar voor uren).
    """

    BASE_URL = "https://secure2.e-boekhouden.nl/bh/"

    def __init__(self, email: str, password: str):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        self._login(email, password)
        self._projects: list[dict] | None = None
        self._activities: list[dict] | None = None

    def _login(self, email: str, password: str) -> None:
        resp = self.session.post(
            self.BASE_URL + "inloggen.asp?login=1",
            data={"txtEmail": email, "txtWachtwoord": password},
        )
        if "U bent nu ingelogd" not in resp.text:
            raise LoginError(
                "Kan niet inloggen bij e-boekhouden.nl. "
                "Controleer je email en wachtwoord in config.yaml."
            )

    def get_projects(self) -> list[dict]:
        """Haal beschikbare projecten op."""
        if self._projects is None:
            self._projects, self._activities = self._parse_uren_form()
        return self._projects

    def get_activities(self) -> list[dict]:
        """Haal beschikbare activiteiten op."""
        if self._activities is None:
            self._projects, self._activities = self._parse_uren_form()
        return self._activities

    def _parse_uren_form(self) -> tuple[list[dict], list[dict]]:
        """Parse het uren invoer formulier voor projecten en activiteiten."""
        resp = self.session.get(self.BASE_URL + "uren.asp?ACTION=ADDNEW")
        soup = BeautifulSoup(resp.content, "html.parser")
        selects = soup.find_all("select")

        projects = self._parse_select_options(selects[0]) if len(selects) > 0 else []
        activities = self._parse_select_options(selects[1]) if len(selects) > 1 else []
        return projects, activities

    @staticmethod
    def _parse_select_options(select_element) -> list[dict]:
        options = []
        for option in select_element.find_all("option"):
            value = option.get("value", "")
            if not value:
                continue
            options.append(
                {
                    "id": int(value),
                    "name": option.text.strip(),
                    "selected": option.has_attr("selected"),
                }
            )
        return options

    def get_default_project_id(self) -> int | None:
        """Geef het ID van het standaard geselecteerde project."""
        for p in self.get_projects():
            if p["selected"]:
                return p["id"]
        return None

    def get_default_activity_id(self) -> int | None:
        """Geef het ID van de standaard geselecteerde activiteit."""
        for a in self.get_activities():
            if a["selected"]:
                return a["id"]
        return None

    def add_hours(
        self,
        hours: float,
        day: date,
        project_id: int,
        activity_id: int,
        comment: str = "",
    ) -> None:
        """Voeg uren toe voor een specifieke dag."""
        payload = {
            "SelActiviteit": activity_id,
            "SelProject": project_id,
            "submit1": "Opslaan",
            "txtAantal": hours,
            "txtDatum": day.strftime("%d-%m-%Y"),
            "txtOpmerkingen": comment,
        }
        self.session.post(
            self.BASE_URL + "uren.asp?ACTION=ADDNEW&SAVE=1&ID=&POPUP=&RETURNURL=",
            data=payload,
        )

    def get_hours(self) -> list[dict]:
        """Haal geregistreerde uren op voor de huidige maand."""
        resp = self.session.get(
            self.BASE_URL + "uren_ov.asp",
            params={"dummy": 1, "ACTION": "LIST"},
        )
        return self._parse_hours_table(resp.content)

    @staticmethod
    def _parse_hours_table(html: bytes) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")

        # De urentabel is typisch de 16e tabel op de pagina
        for table in tables:
            rows = table.find_all("tr")
            if len(rows) < 2:
                continue

            headers = [th.text.strip().lower() for th in rows[0].find_all(["th", "td"])]
            if "datum" not in " ".join(headers) and "uren" not in " ".join(headers):
                continue

            entries = []
            for row in rows[1:]:
                cells = [td.text.strip() for td in row.find_all("td")]
                if len(cells) < 4:
                    continue
                # Zoek ID in links
                link = row.find("a", href=True)
                entry_id = None
                if link:
                    match = re.search(r"ID=(\d+)", link["href"])
                    if match:
                        entry_id = int(match.group(1))
                entries.append(
                    {
                        "id": entry_id,
                        "cells": cells,
                    }
                )
            if entries:
                return entries

        return []
