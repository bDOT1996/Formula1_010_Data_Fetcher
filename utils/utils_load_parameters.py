import logging
import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()  # załaduj .env

def get_snowflake_connection():
    return {
        'user': os.getenv("SF_USER"),
        'password': os.getenv("SF_PASSWORD"),
        'account': os.getenv("SF_ACCOUNT"),
        'warehouse': os.getenv("SF_WAREHOUSE"),
        'database': os.getenv("SF_DATABASE"),
        'schema': os.getenv("SF_SCHEMA")
    }


def get_parameters (input_path):
    input_file = Path(input_path)
    if not input_file.exists():
        logger.error(f"Plik {input_file} nie istnieje.")
        sys.exit(1)

    try:
        logger.info("Odczyt pliku parametrów...")
        with open(input_file, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Błąd w formacie JSON: {e}")
        sys.exit(1)

    return data