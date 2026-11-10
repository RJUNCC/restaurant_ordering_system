import os
from dotenv import load_dotenv

load_dotenv()  # searches upward for .env, so the repo-root .env gets picked up

class conf:
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = int(os.getenv("DB_PORT", "3306"))
    db_name = os.getenv("DB_NAME", "oros")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    app_host = "localhost"
    app_port = 8000
