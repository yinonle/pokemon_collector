import boto3
from typing import List, Dict, Any, Optional
from config import settings

class SqsService():

    def __init__(self, sqs_client = None):
        self.sqs = sqs_client or boto3.client("sqs", region_name = settings.AWS_REGION)

    #def create_sqs(self,):

    #def get_sqs_client():
     #   return boto3.client("sqs", region_name = settings.AWS_REGION)

    def get_messages(self, queue_url: str) -> List[Dict[str, Any]]:
        response = self.sqs.receive_message(QueueUrl = queue_url,MaxNumberOfMessages = 1,WaitTimeSeconds = 10) 
        message = response.get("Messages", [])
        return message

    def send_message(self, queue_url: str, message_body: str) -> Dict[str, Any]:
        response = self.sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
        )
        return response

    def delete_message(self, queue_url: str, receipt_handle: str) -> None:
        self.sqs.delete_message(QueueUrl = queue_url,ReceiptHandle = receipt_handle)
