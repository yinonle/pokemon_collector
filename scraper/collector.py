from typing import Any, Dict, List, Tuple, Union, Optional

from DB.models import PokedexModel
from DB.pokedex import DataBaseHendle
from scheme.validate_requests import (
    CollectorOutputResponse,
    NameCollectionRequest,
    NumberCollectionRequest,
    PokemonModel,
    RangeCollectionRequest,
    SqsMessage,
    sqs_adapter,
)
from scraper.scraper import PokemonScraper
from utils.json_backup import JsonBackupFile


class CollectorService:
    def __init__(
        self,
        pokedex_repo: DataBaseHendle = None,
        scraper: PokemonScraper = None,
        backup_file: JsonBackupFile = None):

        self.pokedex_repo = pokedex_repo or DataBaseHendle()
        self.scraper = scraper or PokemonScraper()
        self.backup_file = backup_file or JsonBackupFile()

    def _extract_identifiers(self, request: SqsMessage) -> Tuple[List[Union[int, str]], List[str]]:
        valid_identifiers = []
        failed_list = []

        if isinstance(request, NameCollectionRequest):
            valid_identifiers.append(request.p_name)

        elif isinstance(request, NumberCollectionRequest):
            num = request.p_number
            if 1 <= num <= 100:
                valid_identifiers.append(num)
            else:
                failed_list.append(str(num))

        elif isinstance(request, RangeCollectionRequest):
            start_str, end_str = request.p_range.split("-")
            start, end = int(start_str), int(end_str)
            for num in range(start, end + 1):
                if 1 <= num <= 100:
                    valid_identifiers.append(num)
                else:
                    failed_list.append(str(num))

        return valid_identifiers, failed_list

    def save_to_model(self,raw_db_pokemon: PokedexModel) -> PokemonModel:
         return PokemonModel(
                serial_number = raw_db_pokemon.serial_number,
                name = raw_db_pokemon.name,
                type = raw_db_pokemon.type,
                weight = raw_db_pokemon.weight,
                height = raw_db_pokemon.height,
                evolution_links = raw_db_pokemon.evolution_links or [],
            ) 

    async def get_pokemon(self, identifier: str | int) -> Tuple[Optional[PokemonModel], bool]:
        db_pokemon = self.pokedex_repo.get_pokemon_from_db(identifier)
        if db_pokemon:
            return self.save_to_model(db_pokemon), True
        
        try:
            scraped_pokemon = await self.scraper.scrape_pokemon(identifier) 
            if scraped_pokemon:
                pokemon_model = PokemonModel(**scraped_pokemon)
                self.pokedex_repo.save_pokemon_to_db(pokemon_model)
                return pokemon_model, False
        except Exception as e:
            raise e
        return None, False

    async def process_collection_request(self, request_data: Dict[str, Any]) -> CollectorOutputResponse:
        count_from_cache = 0
        count_from_website = 0
        pokelist = []

        parsed_request = sqs_adapter.validate_python(request_data)
        collection_id = parsed_request.collection_id
        valid_identifiers, failed_list = self._extract_identifiers(parsed_request)

        for identifier in valid_identifiers:
            pokemon_model , is_from_cache = await self.get_pokemon(identifier)
            if pokemon_model:
                pokelist.append(pokemon_model)
                if is_from_cache:
                    count_from_cache += 1
                else:
                    count_from_website += 1
            else:
                failed_list.append(str(identifier))

        if pokelist:
            self.backup_file.save_pokemon_to_json(pokelist)

        status = ""
        if not failed_list:
            status = "SUCCESS"
        else:
            status = "FAILED"

        self.pokedex_repo.save_to_receipt(
            collection_id = str(collection_id),
            collection_status = status,
            collection_count_from_cache = count_from_cache,
            collection_count_from_website = count_from_website,
        )

        return CollectorOutputResponse(
            collection_id = collection_id, pokelist = pokelist, failed_list = failed_list)
