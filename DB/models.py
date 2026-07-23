from sqlalchemy import Column, DateTime, Integer, String, Text, JSON
from sqlalchemy.sql import func
from DB.data_base import Base


class PokedexModel(Base):
    __tablename__ = "pokedex"

    p_number = Column(Integer, primary_key = True, index = True)
    p_name = Column(String(100), unique = True, nullable = False, index = True)
    types = Column(JSON)
    height = Column(String(50))
    weight = Column(String(50))
    evolutions = Column(JSON)
    created_at = Column(DateTime, server_default = func.now())


class ReceiptModel(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key = True, autoincrement = True)
    pokemon_name = Column(String(100), nullable = True)
    status = Column(String(50), nullable = False)  
    timestamp = Column(DateTime, server_default = func.now())
