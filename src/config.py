from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    DATABASE_URI: str = os.getenv("DATABASE_URI")
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "False").lower() in ("true", "1", "t")
