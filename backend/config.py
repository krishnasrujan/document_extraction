import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    VISION_MODEL = os.getenv(
        "DOCCONF_VISION_MODEL",
        "gpt-4o"
    )
    ARTIFACT_DIR = os.getenv(
        "ARTIFACT_DIR",
        "artifacts"
    )

settings = Settings()