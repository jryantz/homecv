import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    HOMEASSISTANT_URL = os.getenv("HOMEASSISTANT_URL", "")
    HOMEASSISTANT_TOKEN = os.getenv("HOMEASSISTANT_TOKEN", "default-token")

    MODEL_PATH = os.getenv("MODEL_PATH", "./homecv/models/yolo11n.pt")
