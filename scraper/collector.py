from typing import Any, Dict, List, Tuple, Union

from DB.pokedex import PokedexRepository
from scraper.scraper import PokemonScraper
from utils.json_backup import JsonBackupFile
from scheme.validate_requests import CollectorOutputResponse, PokemonModel,SqsMessage, sqs_adapter
from scheme.validate_requests import  NameCollectionRequest, NumberCollectionRequest, RangeCollectionRequest


class CollectorService:
    def __init__(self, 
                pokedex_repo: PokedexRepository = None,
                scraper: PokemonScraper = None, 
                backup_file: JsonBackupFile = None):
        
        self.pokedex_repo = pokedex_repo or PokedexRepository()
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



    def process_collection_request(self, request_data: Dict[str, Any]) -> CollectorOutputResponse:

        count_from_cache = 0
        count_from_website = 0

        pokelist = []
        new_pokemon = []

        #validate our requests.
        parsed_request = sqs_adapter.validate_python(request_data)
        collection_id = parsed_request.collection_id
        valid_identifiers, failed_list = self._extract_identifiers(parsed_request)

        for identifier in valid_identifiers:
            db_pokemon = self.pokedex_repo.get_pokemon_from_db(identifier)

#pokemon is in the DB
            if db_pokemon:
                pokemon_model = PokemonModel(
                    serial_number = db_pokemon.serial_number,
                    name = db_pokemon.name,
                    type = db_pokemon.type,
                    weight = db_pokemon.weight,
                    height = db_pokemon.height,
                    evolution_links = db_pokemon.evolution_links or [],)
                
                pokelist.append(pokemon_model)
                count_from_cache += 1
#pokemon not in DB - cache miss
            else:
                try:
                    scraped_pokemon = self.scraper.scrape_pokemon(identifier)

                    if scraped_pokemon:
                        self.pokedex_repo.save_pokemon_to_db(scraped_pokemon)
                        pokemon_model = PokemonModel(**scraped_pokemon)

                        pokelist.append(pokemon_model)
                        new_pokemon.append(scraped_pokemon)
                        count_from_website += 1
                    else:
                        failed_list.append(str(identifier))
                except Exception:
                    failed_list.append(str(identifier))

    #saving to json
        if new_pokemon:
            self.backup_file.save_pokemon_batch(new_pokemon)

        status = ""
        if not failed_list:
            status = "SUCCESS"
        elif pokelist:
            status = "PARTIAL_SUCCESS"
        else:
            status = "FAILED"

        self.pokedex_repo.save_to_receipt(
            collection_id = str(collection_id),
            collection_status = status,
            collection_count_from_cache = count_from_cache,
            collection_count_from_website = count_from_website)
        
        return CollectorOutputResponse(
            collection_id = collection_id,
            pokelist = pokelist,
            failed_list= failed_list)



            






        
        


    # 1. identify the request by the obj
    # 2. parse the range request
    # 3. move on all the var each request parse to a list
