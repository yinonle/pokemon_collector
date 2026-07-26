import boto3

from config import settings


def get_sqs_client():
    return boto3.client("sqs", region_name = settings.AWS_REGION)

def create_sqs():
    client = get_sqs_client()
    response = client.create_queue(QueueName = settings.INPUT_QUEUE_NAME)

    print(response)
    return response["QueueUrl"]

