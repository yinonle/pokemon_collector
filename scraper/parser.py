from typing import Any, Dict, Union
from bs4 import BeautifulSoup

class ParserPokemon_Page:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def parse_pokemon_page(self, content_page: str) -> Dict[str, Any]:

        soup = BeautifulSoup(content_page, "html.parser")
        vitals_table = soup.select_one("table.vitals_table")
        
        if not vitals_table:
            raise ValueError("vitals table are not found on pokemon page.")

        return {
            "serial_number": self._extract_serial_number(vitals_table),
            "name": self._extract_name(soup),
            "type": self._extract_types(vitals_table),
            "weight": self._extract_vital_field(vitals_table, "Weight"),
            "height": self._extract_vital_field(vitals_table, "Height"),
            "evolution_links": self._extract_evolutions(soup),
        }

            
    def _extract_serial_number(self, vitals_table: BeautifulSoup) -> int:
        strong = vitals_table.select_one("strong")
        return (int(strong.text.replace("#",""))if strong else 0)
    
    def _extract_name(self,soup: BeautifulSoup) -> str:
        h1 = soup.select_one("h1")
        return h1.text.strip() if h1 else ""
    
    def _extract_types(self, vitals_table: BeautifulSoup) -> str:
        types = [a.text.strip() for a in vitals_table.select("a.type-icon")]
        return "/".join(types)

    def _extract_vital_field(self, vitals_table: BeautifulSoup, field_name: str) -> str:
        for row in vitals_table.select("tr"):
            th = row.select_one("th")
            if th and th.text.strip().lower() == field_name.lower():
                td = row.select_one("td")
                if td:
                    return td.text.split("(")[0].strip()
        return ""

    def _extract_evolutions(self, soup: BeautifulSoup) -> List[str]:
        evo_links = soup.select("div.infocard-list-evo a.ent-name")
        return [f"{self.base_url}{a['href']}" for a in evo_links if a.get("href")]
    