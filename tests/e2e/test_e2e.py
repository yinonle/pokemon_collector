import json
import uuid
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from moto import mock_aws

from DB.pokedex import DataBaseHendle
from scraper.collector import CollectorService
from message_processor import MessageProcessor
from sqs.create_sqs import SqsService
from config import settings


@pytest.fixture
def mock_scraper():

    scraper = AsyncMock()
    scraper.scrape_pokemon.side_effect = lambda identifier: {
        "serial_number": int(identifier) if str(identifier).isdigit() else 25,
        "name": f"pokemon_{identifier}",
        "type": "electric",
        "weight": "6.0 kg",
        "height": "0.4 m",
        "evolution_links": ["raichu"]
    }
    return scraper


@pytest_asyncio.fixture
async def db_handle():
    db = DataBaseHendle()
    await db.init_db()
    await db.clear_all_tables()
    yield db
    await db.engine.dispose()


@pytest.mark.asyncio
async def test_successful_pokemon_collection_lifecycle(mock_scraper, db_handle):
    
    with mock_aws():
        sqs_service = SqsService()
        input_url = sqs_service.create_queue(settings.INPUT_QUEUE_NAME)
        output_url = sqs_service.create_queue(settings.OUTPUT_QUEUE_NAME)

        collector_service = CollectorService(pokedex_repo=db_handle, scraper=mock_scraper)
        processor = MessageProcessor(sqs_service=sqs_service, collector_service=collector_service)

        collection_id = str(uuid.uuid4())
        valid_payload = {
            "collection_type": "pokemon_range",
            "collection_id": collection_id,
            "p_range": "1-2"
        }

        sqs_service.send_message(input_url, json.dumps(valid_payload))

        results = await processor.process_messages(input_url, output_url)

        assert results is not None
        assert len(results) == 1
        assert results[0]["valid"] is True

        output_messages = sqs_service.get_messages(output_url)
        assert len(output_messages) == 1
        
        parsed_output = json.loads(output_messages[0]["Body"])
        assert parsed_output["collection_id"] == collection_id
        assert len(parsed_output["pokelist"]) == 2

        pokemon_1 = await db_handle.get_pokemon_from_db(1)
        pokemon_2 = await db_handle.get_pokemon_from_db(2)
        assert pokemon_1 is not None
        assert pokemon_2 is not None
        assert pokemon_1.name == "pokemon_1"
        assert pokemon_2.name == "pokemon_2"

        receipts = await db_handle.get_all_receipts()
        assert len(receipts) == 1
        assert receipts[0].collection_id == collection_id
        assert receipts[0].collection_status == "SUCCESS"
        assert receipts[0].collection_count_from_website == 2


@pytest.mark.asyncio
async def test_invalid_payload_error_handling(mock_scraper, db_handle):
    
    with mock_aws():
        sqs_service = SqsService()
        input_url = sqs_service.create_queue(settings.INPUT_QUEUE_NAME)
        output_url = sqs_service.create_queue(settings.OUTPUT_QUEUE_NAME)

        collector_service = CollectorService(pokedex_repo=db_handle, scraper=mock_scraper)
        processor = MessageProcessor(sqs_service=sqs_service, collector_service=collector_service)

        corrupted_payload = {"invalid_field": "test_data"}
        sqs_service.send_message(input_url, json.dumps(corrupted_payload))

        results = await processor.process_messages(input_url, output_url)

        assert results is not None
        assert len(results) == 1
        assert results[0]["valid"] is False
        assert results[0]["error"] is not None

        output_messages = sqs_service.get_messages(output_url)
        assert len(output_messages) == 0

        receipts = await db_handle.get_all_receipts()
        assert len(receipts) == 0