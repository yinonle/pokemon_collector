import boto3 
from moto import mock_aws
 

@mock_aws
def create_sqs():
    sqs_client = boto3.client('sqs',region_name = 'us-east-1')

    response = sqs_client.create_queue(QueueName="sqs_in")
    queue_url = response["QueueUrl"]

    return queue_url


