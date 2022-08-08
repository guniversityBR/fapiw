from datetime import datetime

from core.configs import settings

from sqlalchemy import Column, Integer, String, DateTime


class ProjetoModel(settings.DBBaseModel):
    """No website temos um portfólio de projetos"""
    __tablename__: str = 'projetos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    data: datetime = Column(DateTime, default=datetime.now, index=True)
    
    titulo: str = Column(String(100))
    descricao_inicial: str = Column(String(300))
    imagem1: str = Column(String(100)) # 1300x700
    imagem2: str = Column(String(100)) # 600x400
    imagem3: str = Column(String(100)) # 600x400
    descricao_final: str = Column(String(300))
    link: str = Column(String(200))

