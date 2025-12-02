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
    PAYMENT_SERVICE_URL = read_env_variable("PAYMENT_SERVICE_URL", True)
    OTEL_SERVICE_NAME = read_env_variable("OTEL_SERVICE_NAME", True)
    DB_CONNECTION_STRING = read_env_variable("DB_CONNECTION_STRING", True)
    USE_CISCO_API = read_env_variable("USE_CISCO_API", True)
    CISCO_CLIENT_ID = read_env_variable("CISCO_CLIENT_ID", False)
    CISCO_CLIENT_SECRET = read_env_variable("CISCO_CLIENT_SECRET", False)
    CISCO_APP_KEY = read_env_variable("CISCO_APP_KEY", False)

settings = Settings()