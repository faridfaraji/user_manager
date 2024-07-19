from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "My FastAPI Application"
    debug: bool = False
    database_url: str = "http://127.0.0.1:9002/v1"
    chat_url: str = "http://127.0.0.1:9000"
    assistant_id: str = "asst_Cokj3GT7qpogbFV1xzmtTbqv"
    celery_broker_url: str = "redis://localhost:6379"
