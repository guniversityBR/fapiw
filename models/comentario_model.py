from datetime import datetime

import sqlalchemy.orm as orm

from core.configs import settings
from models.post_model import PostModel

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class ComentarioModel(settings.DBBaseModel):
    __tablename__: str = 'comentarios'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: datetime = Column(DateTime, default=datetime.now, index=True)

    id_post: int = Column(Integer, ForeignKey('posts.id'))
    post: PostModel = orm.relationship('PostModel', lazy='joined')

    autor: str = Column(String(200))
    texto: str = Column(String(400))
