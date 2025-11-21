import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Career Coach"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    AF_API_BASE_URL: str = "https://jobsearch.api.jobtechdev.se"

    class Config:
        env_file = ".env"

settings = Settings()
