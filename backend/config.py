import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ARTIFACT_DIR = os.getenv(
        "ARTIFACT_DIR",
        "artifacts"
    )

settings = Settings()