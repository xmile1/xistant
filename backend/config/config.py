from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    open_api_key: Optional[str]
    grocy_api_url: str = ""
    grocy_api_key: Optional[str]
    german_speaker_url: Optional[str] = ""
    nigerian_speaker_url: Optional[str] = ""
    rhasspy_listen_for_command_url: Optional[str] = ""

    class Config:
        env_file = ".env"


settings = Settings()
