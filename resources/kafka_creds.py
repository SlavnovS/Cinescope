import os
from dotenv import load_dotenv

load_dotenv()


class KafkaCreds:
    HOST = os.getenv('KAFKA_HOST')
    PORT = os.getenv('KAFKA_PORT')


