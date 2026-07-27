import os
import pytest
from utils.json_backup import JsonBackupHandler


class TestJsonBackupHandler:
    """Unit tests for JsonBackupHandler verifying local JSON persistence and key formatting."""

    def test_load_backup_returns_empty_dict_when_file_does_not_exist(self, tmp_path):
        """Tests that loading a non-existent file returns an empty dictionary without errors."""
        test_file = tmp_path / "non_existent_pokedex.json"
        handler = JsonBackupHandler(file_path=str(test_file))

        data = handler.load_backup()

        assert data == {}
        assert not os.path.exists(test_file)

    def test_save_pokemon_batch_creates_file_and_formats_keys(self, tmp_path):
        """Tests that saving a batch correctly pads serial numbers to 3-digit string keys ('001', '025')."""
        test_file = tmp_path / "pokedex_backup.json"
        handler = JsonBackupHandler(file_path=str(test_file))

        sample_pokemons = [
            {
                "serial_number": 1,
                "name": "Bulbasaur",
                "type": "Grass/Poison",
                "weight": "6.9 kg",
                "height": "0.7 m",
                "evolution_links": ["https://pokemondb.net/pokedex/ivysaur"]
            },
            {
                "serial_number": 25,
                "name": "Pikachu",
                "type": "Electric",
                "weight": "6.0 kg",
                "height": "0.4 m",
                "evolution_links": []
            }
        ]

        handler.save_pokemon_batch(sample_pokemons)

        data = handler.load_backup()

        assert "001" in data
        assert "025" in data
        assert data["001"]["name"] == "Bulbasaur"
        assert data["025"]["name"] == "Pikachu"
        assert data["001"]["serial_number"] == 1

    def test_save_pokemon_batch_merges_with_existing_records(self, tmp_path):
        """Tests that subsequent batch saves merge new items without overwriting existing entries."""
        test_file = tmp_path / "pokedex_backup.json"
        handler = JsonBackupHandler(file_path=str(test_file))

        # First batch save
        batch_one = [
            {
                "serial_number": 1,
                "name": "Bulbasaur",
                "type": "Grass/Poison",
                "weight": "6.9 kg",
                "height": "0.7 m",
                "evolution_links": []
            }
        ]
        handler.save_pokemon_batch(batch_one)

        # Second batch save
        batch_two = [
            {
                "serial_number": 4,
                "name": "Charmander",
                "type": "Fire",
                "weight": "8.5 kg",
                "height": "0.6 m",
                "evolution_links": []
            }
        ]
        handler.save_pokemon_batch(batch_two)

        # Reload and verify both exist
        data = handler.load_backup()

        assert len(data) == 2
        assert "001" in data
        assert "004" in data
        assert data["001"]["name"] == "Bulbasaur"
        assert data["004"]["name"] == "Charmander"