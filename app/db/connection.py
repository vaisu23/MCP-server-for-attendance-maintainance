import os
import time
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

root = Path(__file__).resolve().parent.parent.parent
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(root / env_file)


def get_connection():

    max_retries = 10

    for attempt in range(max_retries):

        try:

            print(f"[DB] Connecting to: {os.getenv('DB_NAME')} (Attempt {attempt + 1})")

            return psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
            )

        except psycopg2.OperationalError as e:

            if attempt == max_retries - 1:
                raise

            print("Database not ready. Retrying in 2 seconds...")
            time.sleep(2)