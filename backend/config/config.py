from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    open_api_key: Optional[str]
    grocy_api_url: str = ""
    grocy_api_key: Optional[str]

    class Config:
        env_file = ".env"


settings = Settings()
