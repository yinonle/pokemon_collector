import boto3
import json

def get_sqs_client():
    return boto3.client("sqs", region_name = "us-east-1")

def create_sqs():
    client = get_sqs_client()
    response = client.create_queue(QueueName = "sqs_in")
    return response["QueueUrl"]

def send_message(queue_url, body):
    client = get_sqs_client()
    return client.send_message(QueueUrl = queue_url, MessageBody = json.dumps(body))