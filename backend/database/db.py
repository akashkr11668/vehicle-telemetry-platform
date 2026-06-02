import psycopg2
import logging
import time

import os

connection = None

# while connection is None:

try:

    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    cursor = connection.cursor()

except Exception as error:

    logging.error(f"Database connection failed: {error}")

    connection = None
    cursor = None
