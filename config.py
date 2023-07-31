from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

simple_db = {
    'users': {
        'john@email.com': {
            'password': '12345secret'
        }
    },
    'sessions': {},
    'dbs': {
        'msisdn': {},
        'sim': {}
    }
}


class Settings(BaseSettings):
    app_name: str = "My Fastapi App"
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    return Settings()
