import sqlalchemy.orm as orm

from core.configs import settings
from models.area_model import AreaModel

from sqlalchemy import Column, Integer, String, ForeignKey


class DuvidaModel(settings.DBBaseModel):
    __tablename__: str = 'duvida'

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    id_area: int = Column(Integer, ForeignKey('areas.id'))
    area: AreaModel = orm.relationship('AreaModel', lazy='joined')

    titulo: str = Column(String(200))
    resposta: str = Column(String(400))

    

