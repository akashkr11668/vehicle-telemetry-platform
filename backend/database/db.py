import psycopg2
import logging
import time

import os

connection = None

while connection is None:

    try:

        connection = psycopg2.connect(
            host="database",
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD")
)

        logging.info("Database connected successfully")

    except Exception as error:

        logging.error(f"Database connection failed: {error}")

        print("Database not ready yet... Retrying in 5 seconds")

        time.sleep(5)

cursor = connection.cursor()