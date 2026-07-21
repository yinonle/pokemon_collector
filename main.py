import uuid
from moto import mock_aws

from sqs_in.create_sqs import create_sqs, get_sqs_client
from sqs_in.producer import send_message
from sqs_in.consumer import delete_message
from message_processor import process_message


@mock_aws
def main():

    queue_url = create_sqs()

    message1 = {
        "collection_type": "pokemon_number",
        "collection_id": str(uuid.uuid4()), 
        "p_number": 3
    }
    send_message(queue_url, message1)

    results = process_message(queue_url)

    if results:
        for res in results:
            print(f"2. validation success? {res['valid']}\n")
            print(f"3. Object Pydantic: {res['data']}\n")
            print(f"4. ID of the: (ReceiptHandle): {res['receipt_handle']}\n")

            delete_message(queue_url, res["receipt_handle"])
            print("5. Message delete from SQS!\n")
    else:
        print("Empty queue\n")

if __name__ == "__main__":
    main()