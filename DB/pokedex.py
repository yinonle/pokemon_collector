from DB.data_base import SessionLocal, Base, engine
from DB.models import PokedexModel, ReceiptModel


def init_db():
    Base.metadata.create_all(bind = engine)


