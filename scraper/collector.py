from typing import Any, Dict, List, Tuple, Union

from DB.pokedex import PokedexRepository
from scraper.scraper import PokemonScraper
from utils.json_backup import JsonBackupFile
from scheme.validate_requests import CollectorOutputResponse, SqsMessage
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
        
        


    # 1. identify the request by the obj
    # 2. parse the range request
    # 3. move on all the var each request parse to a list
    #  
    # 