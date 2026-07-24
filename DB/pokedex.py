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

def save_pokemon_to_db(pokemon_data: dict):
    db = SessionLocal()

    try:
        new_pokemon = PokedexModel(
        p_number = pokemon_data.get("p_number"),
        p_name = pokemon_data.get("p_name"),
        types = pokemon_data.get("types", []),
        height = str(pokemon_data.get("height", "")),
        weight = str(pokemon_data.get("weight", "")),
        evolutions = pokemon_data.get("evolutions", []),)
        db.add(new_pokemon)
        db.commit()
        db.refresh(new_pokemon)

    except Exception as e:
        db.rollback()
        raise e
    
    finally:
        db.close()






