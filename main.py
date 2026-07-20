import uuid
from moto import mock_aws
from sqs_handler import create_sqs, send_message
from schemas.validate_request import SqsMessage

@mock_aws
def main():
    # 1. יצירת הודעה עם UUID תקין
    raw_body = {
        "collection_type": "name",
        "collection_id": str(uuid.uuid4()),  # תיקון ל-UUID תקין
        "p_name": "pikachu"
    }

    validated_message = SqsMessage.model_validate(raw_body)
    print(f"Validated Successfully: {validated_message}")

    queue_url = create_sqs()
    send_message(queue_url, raw_body)
    print(f"Message sent to queue: {queue_url}")

if __name__ == "__main__":
    main()