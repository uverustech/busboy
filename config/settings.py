from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # General settings
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(True, env="DEBUG")
    app_name: str = Field("starfish", env="APP_NAME")

    # MongoDB settings
    mongo_uri: str = Field(..., env="MONGO_URI")
    mongo_db: str = Field("raw_data", env="MONGO_DB")

    # PostgreSQL settings
    postgres_uri: str = Field(..., env="POSTGRES_URI")
    
    # Redis settings
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_db: int = Field(0, env="REDIS_DB")
    redis_password: str = Field(..., env="REDIS_PASSWORD")

    # MinIO settings
    minio_endpoint: str = Field(..., env="MINIO_ENDPOINT")
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")
    minio_bucket: str = Field("cached-images", env="MINIO_BUCKET")

    # Logging settings
    log_level: str = Field("INFO", env="LOG_LEVEL")
    loki_url: str = Field(None, env="LOKI_URL")  # URL to send logs to Loki, if needed

    class Config:
        env_file = ".env"

# Instantiate settings object
settings = Settings()
