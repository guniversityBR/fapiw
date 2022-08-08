from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from fastapi.templating import Jinja2Templates
from pathlib import Path


class Settings(BaseSettings):
    DB_URL: str = 'postgresql+asyncpg://geek:university@localhost:5432/startupgeek'
    DBBaseModel = declarative_base()
    TEMPLATES = Jinja2Templates(directory='templates')
    MEDIA = Path('media')
    AUTH_COOKIE_NAME: str = 'guniversity'
    SALTY: str = 'AnyKwYandMA7o6Cz0MTksByXHriT2fRuAO2p-0y3SbhR3Ou1PnItPFX7zL3cXo861PA9ByalGBneR7O27QRvWw'

    class Config:
        case_sensitive = True



settings: Settings = Settings()
