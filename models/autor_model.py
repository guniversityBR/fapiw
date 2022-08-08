from typing import List

import sqlalchemy.orm as orm
from sqlalchemy import Table, Column, Integer, String, ForeignKey

from core.configs import settings
from models.tag_model import TagModel


# Autor pode ter várias tags
tags_autor = Table(
    'tags_autor',
    settings.DBBaseModel.metadata,
    Column('id_autor', Integer, ForeignKey('autores.id')),
    Column('id_tag', Integer, ForeignKey('tags.id'))
)


class AutorModel(settings.DBBaseModel):
    """Autor das postagens no blog"""
    __tablename__: str = 'autores'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(100))
    imagem: str = Column(String(100)) # 40x40

    # Um autor pode ter várias tags
    tags: List[TagModel] = orm.relationship('TagModel', secondary=tags_autor, backref='taga', lazy='joined')
    
    @property
    def get_tags_list(self):
        lista: List[int] = []

        for tag in self.tags:
            lista.append(int(tag.id))
        
        return lista
