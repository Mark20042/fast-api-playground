from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str = "vault"
    jwt_secret_key: str
    jwt_algorithm: str

    class Config:
        env_file = ".env"
        


settings = Settings()