from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    # The Path start from backend, where we execute uvicorn. So ".." is "email_summarizer_agent" 
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

settings = Settings()