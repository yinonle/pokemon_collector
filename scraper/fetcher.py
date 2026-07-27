from typing import Union
import httpx
from scheme.config import settings


class PokemonFetcher:

    def __init__(self, base_url: str = settings.POKEMON_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.headers = {"User-Agent": settings.USER_AGENT}
        
    def fetch_pokemon_html(self,identifier: Union[str, int]) -> str:
        url = f"{self.base_url}/pokedex/{identifier}"

        with httpx.Client(headers = self.headers, follow_redirects = True, timeout = 10.0) as client:
            response = client.get(url)

            if response.status_code == 404: 
                raise ValueError(f"Pokemon '{identifier}' not found on pokemondb.net")
            
            response.raise_for_status()
        return response.text
    











        
        





