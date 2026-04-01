from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "John Project API"
    CORS_ORIGINS: str = "http://localhost:5173"
    DATABASE_URL: str = "sqlite:///./app.db"


settings = Settings()
