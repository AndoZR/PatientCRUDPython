import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Use SQLite as default for easier testing, can be overridden with DATABASE_URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hospital.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()
