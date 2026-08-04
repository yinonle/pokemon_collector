from sqlalchemy import JSON, Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class PokedexModel(Base):
    __tablename__ = "pokedex"

    serial_number = Column(Integer, primary_key = True, index = True)  
    name = Column(String, unique = True, nullable = False, index = True)
    type = Column(JSON)  
    height = Column(String)
    weight = Column(String)
    evolution_links = Column(JSON) 


class ReceiptModel(Base):
    __tablename__ = "receipt"

    collection_id = Column(String, primary_key = True)
    collection_time = Column(DateTime, server_default = func.now())
    collection_status = Column(String, nullable = False)
    collection_count_from_cache = Column(Integer, default = 0, nullable = False)
    collection_count_from_website = Column(Integer, default = 0, nullable = False)