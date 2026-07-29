import json

from scheme.validate_requests import sqs_adapter
from sqs_in.consumer import get_messages, delete_message
from sqs_in.producer import send_message
from scraper.collector import CollectorService

collector_service  = CollectorService()
def process_message(input_queue_url: str, output_queue_url: str):
    #get the message from the sqs
    messages = get_messages(input_queue_url)

    #Checking the sqs
    if not messages:
        print("There are no requests in the sqs!")
        return None

    results = []
    for message in messages:

        message_body = message["Body"]
        receipt_handle = message.get("ReceiptHandle")
        
        try:
            message_dict = json.loads(message_body)
            #validated = sqs_adapter.validate_python(message_dict)

            response_model = collector_service.process_collection_request(message_dict)           

            output_json = response_model.model_dump_json()
            send_message(output_queue_url, output_json)

            if receipt_handle:
                delete_message(input_queue_url, receipt_handle)

            results.append({"valid": True, "data": response_model, "error": None})            
            
        except Exception as e:
            results.append({"valid": False, "data": None, "error": str(e)})   
             
    return results  