import uuid
from moto import mock_aws
from sqs_in.create_sqs import create_sqs, send_message
from scheme.validate_requests import SqsMessage, sqs_adapter

@mock_aws
def main():

    message1 = {
        "collection_type": "pokemon_number",
        "collection_id": str(uuid.uuid4()), 
        "p_number": 3
    }

    message2 = {
        "collection_type": "e",
        "collection_id": str(uuid.uuid4()), 
        "p_name": "pikac"
    }
    validated_message = sqs_adapter.validate_python(message1)
    print(f"Validated successfully: {validated_message}")

    queue_url = create_sqs()
    send_message(queue_url, message1)
    #send_message(queue_url, message1)

    print(f"Message sent to queue: {queue_url}")

if __name__ == "__main__":
    main()