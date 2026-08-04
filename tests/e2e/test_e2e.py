import json
import uuid
import pytest
from moto import mock_aws

from message_processor import MessageProcessor
from sqs.create_sqs import SqsService
from DB.pokedex import DataBaseHendle
from config import settings


@pytest.fixture
def sqs_setup():
    with mock_aws():
        sqs_service = SqsService()
        input_url = sqs_service.create_queue(settings.INPUT_QUEUE_NAME)
        output_url = sqs_service.create_queue(settings.OUTPUT_QUEUE_NAME)
        
        yield {
            "sqs": sqs_service,
            "input_url": input_url,
            "output_url": output_url
        }


@mock_aws
def test_e2e_successful_pokemon_collection(sqs_setup):

    DataBaseHendle.init_db()

    sqs_service = sqs_setup["sqs"]
    input_url = sqs_setup["input_url"]
    output_url = sqs_setup["output_url"]
    
    test_id = str(uuid.uuid4())
    payload = {
        "collection_type": "name",
        "collection_id": test_id,
        "p_name": "pikachu"
    }
    sqs_service.send_message(input_url, json.dumps(payload))

    
    processor = MessageProcessor(sqs_service = sqs_service)
    results = processor.process_messages(input_url, output_url)

    
    assert results is not None
    assert results[0]["valid"] is True, f"Processor error: {results[0]['error']}"
    
    outputs = sqs_service.get_messages(output_url)
    assert len(outputs) == 1
    
    data = json.loads(outputs[0]["Body"])
    assert data["collection_id"] == test_id