import boto3
from moto import mock_aws

from scheme.validate_requests import get_sqs_client


def receive_messages(queue_url):
    client = get_sqs_client()

    response = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10) 
    message = response.get("Messages", [])
    return message
    
    
        
    