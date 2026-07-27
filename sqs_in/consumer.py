from sqs_in.create_sqs import get_sqs_client

#Input url_sqs and I return the messages
def get_messages(queue_url):
    client = get_sqs_client()

    response = client.receive_message(QueueUrl = queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10) 
    message = response.get("Messages", [])
    return message


def delete_message(queue_url, receipt_handle):
    client = get_sqs_client()
    client.delete_message(QueueUrl=queue_url,ReceiptHandle=receipt_handle)

#raw_message = receive_messages(queue_url)
#  
    