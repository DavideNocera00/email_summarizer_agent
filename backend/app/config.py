from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str
    session_secret: str
    encryption_key: str
    google_api_key: str
    gemini_model: str = "gemini-3.6-flash"
    # The Path start from backend, where we execute uvicorn. So ".." is "email_summarizer_agent" 
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

settings = Settings()