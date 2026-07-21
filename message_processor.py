import json

from scheme.validate_requests import sqs_adapter
from sqs_in.consumer import receive_messages


def process_message(queue_url):
    messages = receive_messages(queue_url)

    if not messages:
        print("There isn't requests in the sqs!")
        return None

    results = []
    for message in messages:
        message_body = message["Body"]
        receipt_handle = message.get("ReceiptHandle")
        
        try:
            message_dict = json.loads(message_body)
            validated = sqs_adapter.validate_python(message_dict)
            results.append({"valid": True, "data": validated, "error": None, "receipt_handle": receipt_handle})
        except Exception as e:
            results.append({"valid": False, "data": None, "error": str(e), "receipt_handle": receipt_handle})
    
    return results  