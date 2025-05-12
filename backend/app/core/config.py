from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My First Platform"
    debug: bool = False
    database_url: str = "sqlite:///./sql_app.db"
    
    class Config:
        env_file = ".env"

settings = Settings()
