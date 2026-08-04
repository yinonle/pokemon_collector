from typing import Union
import httpx
import asyncio
from config import settings


class PokemonFetcher:

    def __init__(self, base_url: str = settings.POKEMON_BASE_URL):
        self.base_url = base_url
        self.headers = {"User-Agent": settings.USER_AGENT}
        
    async def fetch_pokemon_html(self,identifier: Union[str, int]) -> str:
        base = self.base_url.rstrip("/")
        clean_id = str(identifier).strip("/")
        
        if base.endswith("pokedex"):
            url = f"{base}/{clean_id}"
        else:
            url = f"{base}/pokedex/{clean_id}"

        async with httpx.AsyncClient(headers=self.headers, follow_redirects=True, timeout=10.0) as client:
            response = await client.get(url)

            if response.status_code == 404: 
                raise ValueError(f"Pokemon '{identifier}' not found on pokemondb.net")
            
            response.raise_for_status()
        return response.text
    











        
        





