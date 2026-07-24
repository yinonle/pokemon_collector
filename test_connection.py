from DB.data_base import engine
from DB.pokedex import (
    create_receipt,
    get_pokemon_from_db,
    init_db,
    save_pokemon_to_db,
)


def test_db_connection():
    """Tests basic database connection using the SQLAlchemy engine."""
    print("--- 1. Testing Database Connection ---")
    try:
        with engine.connect() as connection:
            print("Database connection success!!!")
            return True
    except Exception as e:
        print("Database connection failed!")
        print(f"Error: {e}")
        return False


def test_init_db():
    """Tests table creation in PostgreSQL."""
    print("\n--- 2. Testing init_db() ---")
    try:
        init_db()
        print("Tables initialized successfully in PostgreSQL!")
    except Exception as e:
        print(f"Failed to initialize tables: {e}")


def test_save_pokemon():
    """Tests saving a mock Pokemon into the database."""
    print("\n--- 3. Testing save_pokemon_to_db() ---")
    sample_pokemon = {
        "p_number": 25,
        "p_name": "Pikachu",
        "types": ["Electric"],
        "height": "0.4m",
        "weight": "6.0kg",
        "evolutions": ["Pichu", "Pikachu", "Raichu"],
    }

    try:
        saved_pokemon = save_pokemon_to_db(sample_pokemon)
        print(f"Successfully saved Pokemon to DB:")
        print(f"  Number: {saved_pokemon.p_number}")
        print(f"  Name: {saved_pokemon.p_name}")
        print(f"  Types: {saved_pokemon.types}")
        return saved_pokemon
    except Exception as e:
        print(f"Failed to save Pokemon: {e}")
        return None


def test_get_pokemon():
    """Tests fetching a Pokemon by name from the database (case-insensitive)."""
    print("\n--- 4. Testing get_pokemon_from_db() ---")
    search_name = "pikachu"
    try:
        pokemon = get_pokemon_from_db(search_name)
        if pokemon:
            print(f"Successfully fetched Pokemon '{search_name}' from DB:")
            print(f"  Found Name: {pokemon.p_name}")
            print(f"  Evolutions: {pokemon.evolutions}")
        else:
            print(f"Pokemon '{search_name}' was not found in the database.")
    except Exception as e:
        print(f"Failed to fetch Pokemon: {e}")


def test_create_receipt():
    """Tests creating an audit receipt record in the database."""
    print("\n--- 5. Testing create_receipt() ---")
    pokemon_name = "pikachu"
    status = "SUCCESS"

    try:
        receipt = create_receipt(pokemon_name=pokemon_name, status=status)
        print("Successfully created receipt record:")
        print(f"  Receipt ID: {receipt.id}")
        print(f"  Pokemon: {receipt.pokemon_name}")
        print(f"  Status: {receipt.status}")
        print(f"  Timestamp: {receipt.timestamp}")
    except Exception as e:
        print(f"Failed to create receipt: {e}")


def run_all_tests():
    """Executes all database test functions sequentially."""
    print("==========================================")
    print("       STARTING DATABASE SUITE TEST       ")
    print("==========================================")

    if test_db_connection():
        test_init_db()
        test_save_pokemon()
        test_get_pokemon()
        test_create_receipt()

    print("\n==========================================")
    print("       FINISHED DATABASE SUITE TEST       ")
    print("==========================================")


if __name__ == "__main__":
    run_all_tests()