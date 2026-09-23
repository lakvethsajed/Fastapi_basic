from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_username : str
    database_hostname : str
    database_name : str
    database_password : str 
    database_port : str
    secret_key : str
    algorithm: str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"

settings = Settings()