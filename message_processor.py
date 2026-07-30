import json
from typing import List, Optional 
from scraper.collector import CollectorService
from sqs.create_sqs import SqsService
from scheme.validate_requests import ProcessResult

collector_service  = CollectorService()
sqs_service = SqsService()

# drains queue out of msgs, runs jobs, returns results
def process_message(input_queue_url: str, output_queue_url: str) -> Optional[List[ProcessResult]]:
    #get the message from the sqs
    messages = sqs_service.get_messages(input_queue_url) # TODO: needs to validate models here, return fully validates msg objects 

    #Checking the sqs
    if not messages:
        print("There are no requests in the sqs!")
        return None

    results = []
    for message in messages:
        # TODO: access validated models via .Body
        message_body = message["Body"]
        receipt_handle = message.get("ReceiptHandle")
        
        try:
            message_dict = json.loads(message_body) # redundant if model is validated
            #validated = sqs_adapter.validate_python(message_dict)

            # type hint list[PokemonModel]
            response = collector_service.process_collection_request(message_dict)           

            output_json = response.model_dump_json()
            sqs_service.send_message(output_queue_url, output_json)

            if receipt_handle:
                sqs_service.delete_message(input_queue_url, receipt_handle)

            # pydnatic response models here, not that bad like this too, but can be improved
            results.append({"valid": True, "data": response, "error": None})            
            
        except Exception as e: 
            results.append({"valid": False, "data":None, "error": str(e)})   

    return results  