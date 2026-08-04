from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DB.models import Base
from DB.models import PokedexModel, ReceiptModel
from scheme.validate_requests import PokemonModel
from config import settings


class DataBaseHendle:

    def __init__(self, db_url: str = settings.DATABASE_URL):
        self.engine = create_engine(db_url)
        self.session_maker = sessionmaker(autocommit = False, autoflush = False, bind = self.engine)

    def init_db(self):
        Base.metadata.create_all(bind = self.engine)

    def get_pokemon_from_db(self, identifier_pok: str | int) -> Optional[PokedexModel]:
        with self.session_maker() as db:
            if isinstance(identifier_pok, int):
                return (db.query(PokedexModel).filter(PokedexModel.serial_number == identifier_pok).first())
                
            elif isinstance(identifier_pok, str) and identifier_pok.isdigit():
                return (db.query(PokedexModel).filter(PokedexModel.serial_number == int(identifier_pok)).first())
    
            else:
                return (db.query(PokedexModel).filter(PokedexModel.name.ilike(identifier_pok)).first())


    def save_pokemon_to_db(self, pokemon_data: PokemonModel) -> PokedexModel:
        with self.session_maker() as db:
            try:
                new_pokemon = PokedexModel(**pokemon_data.model_dump())
                db.add(new_pokemon)
                db.commit()
                return new_pokemon
            except Exception as e:
                raise e
    


    def save_to_receipt(
        self, 
        collection_id: str, 
        collection_status: str, 
        collection_count_from_cache: int = 0, 
        collection_count_from_website: int = 0
    ) -> ReceiptModel:
        
        with self.session_maker() as db:
            try:
                new_receipt = ReceiptModel(
                    collection_id=collection_id,
                    collection_status=collection_status,
                    collection_count_from_cache=collection_count_from_cache,
                    collection_count_from_website=collection_count_from_website,
                )
                db.add(new_receipt)
                db.commit()
                return new_receipt
            except Exception as e:
                raise e

    def get_all_receipts(self):
        with self.session_maker() as db:
            return db.query(ReceiptModel).all()