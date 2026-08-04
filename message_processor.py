import json
from typing import List, Optional 
from scraper.collector import CollectorService
from sqs.create_sqs import SqsService
from scheme.validate_requests import ProcessResult


class MessageProcessor:
    def __init__(self, sqs_service: Optional[SqsService] = None, collector_service: Optional[CollectorService] = None):
        self.sqs_service = sqs_service or SqsService()
        self.collector_service = collector_service or CollectorService()

    async def process_messages(self, input_queue_url: str, output_queue_url: str) -> Optional[List[dict]]:
        messages = self.sqs_service.get_messages(input_queue_url) 
        if not messages:
            print("There are no requests in the sqs!")
            return None

        results = []
        for message in messages:
            message_body = message["Body"]
            receipt_handle = message.get("ReceiptHandle")
            
            try:
                message_dict = json.loads(message_body)
                response = await self.collector_service.process_collection_request(message_dict)
                
                output_json = response.model_dump_json()
                self.sqs_service.send_message(output_queue_url, output_json)

                if receipt_handle:
                    self.sqs_service.delete_message(input_queue_url, receipt_handle)

                results.append({"valid": True, "data": response, "error": None})            
                
            except Exception as e: 
                results.append({"valid": False, "data":None, "error": str(e)})   

        return results  