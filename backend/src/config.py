from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URI: str = os.getenv("DATABASE_URI")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
