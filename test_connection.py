import uuid
from unittest.mock import MagicMock
import pytest

from scraper.collector import CollectorService
from scheme.validate_requests import CollectorOutputResponse


@pytest.fixture
def mock_dependencies():
    """Fixture to create mocked dependencies for CollectorService."""
    mock_repo = MagicMock()
    mock_scraper = MagicMock()
    mock_backup = MagicMock()

    return mock_repo, mock_scraper, mock_backup


@pytest.fixture
def service(mock_dependencies):
    """Fixture to instantiate CollectorService with mocked dependencies."""
    mock_repo, mock_scraper, mock_backup = mock_dependencies
    return CollectorService(
        pokedex_repo=mock_repo,
        scraper=mock_scraper,
        backup_file=mock_backup,
    )


def test_process_range_with_cache_hit_and_out_of_bounds(service, mock_dependencies):
    """
    Test range request ("99-101"):
    - 99: Found in DB (cache hit)
    - 100: Not in DB, scraped successfully (cache miss)
    - 101: Out of allowed range (1-100) -> goes to failed_list
    """
    mock_repo, mock_scraper, mock_backup = mock_dependencies

    # Setup mock behaviors
    mock_pokemon_db = MagicMock()
    mock_pokemon_db.serial_number = 99
    mock_pokemon_db.name = "Kingler"
    mock_pokemon_db.type = "Water"
    mock_pokemon_db.weight = "60.0 kg"
    mock_pokemon_db.height = "1.3 m"
    mock_pokemon_db.evolution_links = []

    # 99 returns DB object, 100 returns None (cache miss)
    mock_repo.get_pokemon_from_db.side_effect = lambda identifier: (
        mock_pokemon_db if identifier == 99 else None
    )

    # 100 is scraped from website
    mock_scraper.scrape_pokemon.return_value = {
        "serial_number": 100,
        "name": "Voltorb",
        "type": "Electric",
        "weight": "10.4 kg",
        "height": "0.5 m",
        "evolution_links": ["Electrode"],
    }

    test_request = {
        "collection_type": "pokemon_range",
        "collection_id": str(uuid.uuid4()),
        "p_range": "99-101",
    }

    # Execute service method
    response = service.process_collection_request(test_request)

    # Assertions
    assert isinstance(response, CollectorOutputResponse)
    assert len(response.pokelist) == 2
    assert response.failed_list == ["101"]

    # Verify repository calls
    mock_backup.save_pokemon_batch.assert_called_once()
    mock_repo.save_to_receipt.assert_called_once_with(
        collection_id=test_request["collection_id"],
        collection_status="PARTIAL_SUCCESS",
        collection_count_from_cache=1,
        collection_count_from_website=1,
    )


def test_process_number_out_of_range(service, mock_dependencies):
    """Test single number request out of allowed range (e.g., 150)."""
    mock_repo, _, _ = mock_dependencies

    test_request = {
        "collection_type": "pokemon_number",
        "collection_id": str(uuid.uuid4()),
        "p_number": 150,
    }

    response = service.process_collection_request(test_request)

    assert len(response.pokelist) == 0
    assert response.failed_list == ["150"]

    # Verify receipt status is FAILED
    mock_repo.save_to_receipt.assert_called_once_with(
        collection_id=test_request["collection_id"],
        collection_status="FAILED",
        collection_count_from_cache=0,
        collection_count_from_website=0,
    )


def test_process_name_request_success(service, mock_dependencies):
    """Test valid name request ("pikachu") retrieved via web scraping."""
    mock_repo, mock_scraper, mock_backup = mock_dependencies

    # Not in cache
    mock_repo.get_pokemon_from_db.return_value = None

    # Scraped successfully
    mock_scraper.scrape_pokemon.return_value = {
        "serial_number": 25,
        "name": "pikachu",
        "type": "Electric",
        "weight": "6.0 kg",
        "height": "0.4 m",
        "evolution_links": ["Raichu"],
    }

    test_request = {
        "collection_type": "name",
        "collection_id": str(uuid.uuid4()),
        "p_name": "pikachu",
    }

    response = service.process_collection_request(test_request)

    assert len(response.pokelist) == 1
    assert response.pokelist[0].name == "pikachu"
    assert response.failed_list == []

    mock_repo.save_pokemon_to_db.assert_called_once()
    mock_backup.save_pokemon_batch.assert_called_once()
    mock_repo.save_to_receipt.assert_called_once_with(
        collection_id=test_request["collection_id"],
        collection_status="SUCCESS",
        collection_count_from_cache=0,
        collection_count_from_website=1,
    )