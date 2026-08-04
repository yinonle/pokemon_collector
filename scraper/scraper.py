from typing import Any, Dict, Union
from config import settings
from scraper.fetcher import PokemonFetcher
from scraper.parser import PokemonParser


class PokemonScraper:

    def __init__(self):
        self.fetcher = PokemonFetcher()
        self.parser = PokemonParser(base_url = settings.POKEMON_BASE_URL)

    async def scrape_pokemon(self, identifier: Union[str, int]) -> Dict[str, Any]:
        html_str = await self.fetcher.fetch_pokemon_html(identifier)
        return self.parser.parse(html_str)
    
