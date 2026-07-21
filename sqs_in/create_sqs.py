import boto3

def get_sqs_client():
    return boto3.client("sqs", region_name = "us-east-1")

def create_sqs():
    client = get_sqs_client()
    response = client.create_queue(QueueName = "sqs_in")
    return response["QueueUrl"]

