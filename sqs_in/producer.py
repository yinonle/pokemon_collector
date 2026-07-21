import json
from sqs_in.create_sqs import get_sqs_client

def send_message(queue_url, body):
    client = get_sqs_client()
    return client.send_message(QueueUrl = queue_url, MessageBody = json.dumps(body))

