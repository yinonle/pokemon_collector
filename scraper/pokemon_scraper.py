from typing import Any, Dict, Union
from bs4 import BeautifulSoup
import httpx

from scheme.config import settings


class PokemonScraper:

    def __init__(self, base_url: str = settings.POKEMON_BASE_URL):
        self.base_url = base_url.rstrip("/")

        self.headers = {"User_agent": settings.USER_AGENT}

    def _fetch_data(self,identifier: Union[str, int]) -> str:

        url = f"{self.base_url}/pokedex/{identifier}"

        with httpx.Client(headers = self.headers, follow_redirects = True, timeout = 10.0) as client:
            response = client.get(url)

            if response.status_code == 404: 
                raise ValueError(f"Pokemon '{identifier}' not found on pokemondb.net")
            
            response.raise_for_status()
        return response.text
    











        
        





