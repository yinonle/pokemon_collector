from DB.data_base import SessionLocal, Base, engine
from DB.models import PokedexModel, ReceiptModel


def init_db():
    Base.metadata.create_all(bind = engine)


def get_pokemon_drom_db(name: str):
    db = SessionLocal()
    try:
        pokemon = (
            db.query(PokedexModel).filter(PokedexModel.p_name.ilike(name)).first())
        return pokemon
    
    finally:
        db.close()


