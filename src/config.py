import logging
import os

import dotenv

PATH_TO_PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PATH_TO_ENV = os.path.join(PATH_TO_PROJECT, '.env')

dotenv.load_dotenv(PATH_TO_ENV)

DB_URL = os.getenv("DB_URL")
TRUSTED_KEY = os.getenv("TRUSTED_KEY")

logging.basicConfig(level=logging.DEBUG)
