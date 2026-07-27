from typing import Optional, Union

from DB.data_base import Base, SessionLocal, engine
from DB.models import PokedexModel, ReceiptModel


class PokedexRepository:

    def __init__(self, session_maker = SessionLocal):
        self.session_maker = session_maker


    @staticmethod
    def init_db():
        Base.metadata.create_all(bind = engine)



    def get_pokemon_from_db(self, identifier_pok: Union[str, int]) -> Optional[PokedexModel]:
        #‹

        with self.session_maker() as db:
            if isinstance(identifier_pok, int):
                return (db.query(PokedexModel).filter(PokedexModel.serial_number == identifier_pok).first())
                
            elif isinstance(identifier_pok, str) and identifier_pok.isdigit():
                return (db.query(PokedexModel).filter(PokedexModel.serial_number == int(identifier_pok)).first())
            
            else:
                return (db.query(PokedexModel).filter(PokedexModel.name.ilike(identifier_pok)).first())


    def save_pokemon_to_db(self, pokemon_data: dict) -> PokedexModel:
        with self.session_maker() as db:
            try:
                new_pokemon = PokedexModel(
                    serial_number = pokemon_data.get("serial_number"),
                    name = pokemon_data.get("name"),
                    type = pokemon_data.get("type"),
                    height = pokemon_data.get("height", ""),
                    weight = pokemon_data.get("weight", ""),
                    evolution_links = pokemon_data.get("evolution_links", []),
                )

                db.add(new_pokemon)
                db.commit()
                db.refresh(new_pokemon)
                return new_pokemon
            
            except Exception as e:
                #db.rollback()
                raise e
    


    def save_to_receipt(self, collection_id: str, status: str, 
                       count_from_cache: int = 0, count_from_website: int = 0,) -> ReceiptModel:
        
        with self.session_maker() as db:
            try:
                new_receipt = ReceiptModel(
                    collection_id = collection_id,
                    collection_status = status,
                    collection_count_from_cache = count_from_cache,
                    collection_count_from_website = count_from_website,
                )
                db.add(new_receipt)
                db.commit()
                db.refresh(new_receipt)
                return new_receipt
            
            except Exception as e:
                #db.rollback()
                raise e
        