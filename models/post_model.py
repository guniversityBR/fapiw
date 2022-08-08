from typing import List
from datetime import datetime

import sqlalchemy.orm as orm

from core.configs import settings
from models.tag_model import TagModel
from models.autor_model import AutorModel

from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey


# Post pode ter várias tags
tags_post = Table(
    'tags_post',
    settings.DBBaseModel.metadata,
    Column('id_post', Integer, ForeignKey('posts.id')),
    Column('id_tag', Integer, ForeignKey('tags.id'))
)

# Post pode ter vários comentários
comentarios_post = Table(
    'comentarios_post',
    settings.DBBaseModel.metadata,
    Column('id_post', Integer, ForeignKey('posts.id')),
    Column('id_comentario', Integer, ForeignKey('comentarios.id'))
)


class PostModel(settings.DBBaseModel):
    """Posts do blog"""
    __tablename__: str = 'posts'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: datetime = Column(DateTime, default=datetime.now, index=True)

    titulo: str = Column(String(200))
    
    # Um Post pode ter várias tags
    tags: List[TagModel] = orm.relationship('TagModel', secondary=tags_post, backref='tagp', lazy='joined')

    imagem: str = Column(String(100)) # 900x400
    texto: str = Column(String(1000))

    # Um Post pode ter vários comentários (Não importamos e usamos ComentarioModel como tipo de dados aqui pois causa erro de import circular com a tabela ComentarioModel)
    comentarios: List[object] = orm.relationship('ComentarioModel', secondary=comentarios_post, backref='comentario', lazy='joined')

    id_autor: int = Column(Integer, ForeignKey('autores.id'))
    autor: AutorModel = orm.relationship('AutorModel', lazy='joined')
    
    @property
    def get_tags_list(self):
        lista: List[int] = []

        for tag in self.tags:
            lista.append(int(tag.id))
        
        return lista
