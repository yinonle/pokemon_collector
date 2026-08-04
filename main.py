import time
import logging
import json
import uuid
from moto import mock_aws
import asyncio

from message_processor import MessageProcessor
from DB.pokedex import DataBaseHendle
from sqs.create_sqs import SqsService
from config import settings


logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")

async def main():

    with mock_aws():
        logging.info("Initializ Database tables...")
        DataBaseHendle().init_db()

        sqs_service = SqsService()
        
        input_queue_url = sqs_service.create_queue(settings.INPUT_QUEUE_NAME)
        output_queue_url = sqs_service.create_queue(settings.OUTPUT_QUEUE_NAME)
        
        logging.info(f"Mock Input Queue URL: {input_queue_url}")
        logging.info(f"Mock Output Queue URL: {output_queue_url}")

        processor = MessageProcessor(sqs_service = sqs_service)

        test_message = {
            "collection_type": "pokemon_range", 
            "collection_id": str(uuid.uuid4()),
            "p_range": "1-10"
        }

        sqs_service.send_message(input_queue_url, json.dumps(test_message))

        logging.info("Pushed initial test message (Pikachu) into Mock SQS!")
        logging.info("Pokemon Collector Worker is running!")

        try:
            while True:
                results = await processor.process_messages(input_queue_url, output_queue_url)
                
                if results:
                    logging.info(f"Processed batch successfully: {len(results)} messages")
                
                await asyncio.sleep(2)
        except KeyboardInterrupt:
            logging.info("Worker stopped by user.")

if __name__ == "__main__":
    asyncio.run(main())

