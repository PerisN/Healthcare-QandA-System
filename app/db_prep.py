import os
from dotenv import load_dotenv
from db import init_db

os.environ['RUN_TIMEZONE_CHECK'] = '0'

load_dotenv()

if __name__ == "__main__":
    print("Initializing database...")
    init_db()