from typing import Optional, List

from fastapi.requests import Request
from sqlalchemy.future import select

from core.database import get_session
from models.duvida_model import DuvidaModel
from models.area_model import AreaModel
from controllers.base_controller import BaseController


class DuvidaController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, DuvidaModel)
    
    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()
        
        # Area
        area_id: int = form.get('area')
        
        titulo: str = form.get('titulo')
        resposta: str = form.get('resposta')

        # Instanciar o objeto
        duvida: DuvidaModel = DuvidaModel(id_area=int(area_id), titulo=titulo, resposta=resposta)
  
        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(duvida)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            duvida: DuvidaModel = await session.get(self.model, obj.id)

            if duvida:
                # Recebe os dados do form
                form = await self.request.form()

                area_id: int = form.get('area')
                titulo: str = form.get('titulo')
                resposta: str = form.get('resposta')

                if area_id and int(area_id) != duvida.id_area:
                    duvida.id_area = int(area_id)
                if titulo and titulo != duvida.titulo:
                    duvida.titulo = titulo
                if resposta and resposta != duvida.resposta:
                    duvida.resposta = resposta
                
                await session.commit()


    @property
    async def get_areas(self):
        """
        Retorna todos os registros de area
        """
        async with get_session() as session:
            query = select(AreaModel)
            result = await session.execute(query)
            areas: Optional[List[AreaModel]] = result.scalars().all()

            return areas

