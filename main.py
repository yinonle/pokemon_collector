import asyncio
import aiohttp


async def main():
    # Create a new Pokemon instance
    pikachu = Pokemon(
        collection_type="pokemon",
        collection_id=1,
        name="Pikachu",
        type="Electric",
        level=5
    )

    

    print(pikachu)