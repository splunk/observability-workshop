import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    PAYMENT_GATEWAY_API_KEY = os.getenv("PAYMENT_GATEWAY_API_KEY", "")
    NOTIFICATION_API_KEY = os.getenv("NOTIFICATION_API_KEY", "")
    ENV = os.getenv("ENV", "dev")

settings = Settings()