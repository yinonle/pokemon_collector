from typing import Any, Dict

from DB.pokedex import PokedexRepository
from scraper.scraper import PokemonScraper
from utils.json_backup import JsonBackupFile
from scheme.validate_requests import CollectorOutputResponse, SqsMessage
from scheme.validate_requests import  NameCollectionRequest, NumberCollectionRequest, RangeCollectionRequest


class CollectorService:
    def __init__(self, 
                 pokedex_repo: PokedexRepository = None,
                  scraper: PokemonScraper = None, 
                  backup_handler: JsonBackupFile = None):
        
        self.pokedex_repo = pokedex_repo or PokedexRepository()
        self.scraper = scraper or PokemonScraper()
        self.backup_handler = backup_handler or JsonBackupFile()


    def _extract_identifiers(self, request: SqsMessage):
        identifiers = []
        failed_list = []

        if isinstance(request, NameCollectionRequest):
            

        elif isinstance(request, NumberCollectionRequest):
            pass

        elif isinstance(request, RangeCollectionRequest):
            pass

        return identifiers, failed_list

    def process_collection_request(self, request_data: Dict[str, Any]) -> CollectorOutputResponse:
        identify()
        


    # 1. identify the request by the obj
    # 2. parse the range request
    # 3. move on all the var each request parse to a list
    #  
    # 