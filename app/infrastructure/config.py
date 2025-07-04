from pydantic_settings import BaseSettings

class Config(BaseSettings):
    openai_api_key: str = ""

    class Config:
        env_file = ".env"

def provide_config() -> Config:
    return Config()