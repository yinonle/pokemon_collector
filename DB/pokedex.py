from typing import Optional
from DB.models import Base
from DB.models import PokedexModel, ReceiptModel
from scheme.validate_requests import PokemonModel
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select, delete

class DataBaseHendle:

    def __init__(self, db_url: str = settings.DATABASE_URL):
        self.engine = create_async_engine(db_url)
        self.session_maker = async_sessionmaker(bind = self.engine, class_ = AsyncSession)

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_pokemon_from_db(self, identifier_pok: str | int) -> Optional[PokedexModel]:
        async with self.session_maker() as db:
            if isinstance(identifier_pok, int):
                query = select(PokedexModel).where(PokedexModel.serial_number == identifier_pok)                
            elif isinstance(identifier_pok, str) and identifier_pok.isdigit():
                query = select(PokedexModel).where(PokedexModel.serial_number == int(identifier_pok))
            else:
                query = select(PokedexModel).where(PokedexModel.name.ilike(identifier_pok))
            result = await db.execute(query)
            return result.scalars().first()


    async def save_pokemon_to_db(self, pokemon_data: PokemonModel) -> PokedexModel:
        async with self.session_maker() as db:
            try:
                new_pokemon = PokedexModel(**pokemon_data.model_dump())
                db.add(new_pokemon)
                await db.commit()
                return new_pokemon
            except Exception as e:
                raise e
    


    async def save_to_receipt(
        self, 
        collection_id: str, 
        collection_status: str, 
        collection_count_from_cache: int = 0, 
        collection_count_from_website: int = 0
    ) -> ReceiptModel:
        
        async with self.session_maker() as db:
            try:
                new_receipt = ReceiptModel(
                    collection_id=collection_id,
                    collection_status=collection_status,
                    collection_count_from_cache=collection_count_from_cache,
                    collection_count_from_website=collection_count_from_website,
                )
                db.add(new_receipt)
                await db.commit()
                return new_receipt
            except Exception as e:
                raise e

    async def get_all_receipts(self):
        async with self.session_maker() as db:
            query = select(ReceiptModel)
            result = await db.execute(query)
            return list(result.scalars().all())

    async def clear_all_tables(self):
        async with self.session_maker() as db:
            await db.execute(delete(ReceiptModel))
            await db.execute(delete(PokedexModel))
            await db.commit()