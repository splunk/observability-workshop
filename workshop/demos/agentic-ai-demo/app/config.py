import os
from dotenv import load_dotenv

load_dotenv()

def read_env_variable(key: str, isRequired: bool):
    value = os.environ.get(key)
    if value is None and isRequired:
        raise Exception(f'{key} environment variable must be set')
    return value

class Settings:
    OPENAI_API_KEY = read_env_variable("OPENAI_API_KEY", True)
    OPENAI_MODEL = read_env_variable("OPENAI_MODEL", True)
    OPENAI_BASE_URL = read_env_variable("OPENAI_BASE_URL", True)
    PAYMENT_GATEWAY_API_KEY = read_env_variable("PAYMENT_GATEWAY_API_KEY", False)
    NOTIFICATION_API_KEY = read_env_variable("NOTIFICATION_API_KEY", False)
    OTEL_SERVICE_NAME = read_env_variable("OTEL_SERVICE_NAME", True)
    DB_CONNECTION_STRING = read_env_variable("DB_CONNECTION_STRING", True)

settings = Settings()