from pydantic import BaseSettings

__all__ = ["get_settings", "Settings", "settings"]


class Settings(BaseSettings):
    PROJECT_ENV: str = "development"
    APP_SECRET_KEY: str
    DATABASE_ACCESS_KEY: str
    DATABASE_SECRET_KEY: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str = "nonooncompany-aloha"
    APP_BUNDLE_IDENTIFIER: str
    KAKAO_ADMIN_KEY: str
    APISTORE_KEY: str
    BASE_URL: str = "http://localhost:8001/"
    FCM_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
