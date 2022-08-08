from fastapi.requests import Request

from core.database import get_session
from models.area_model import AreaModel
from controllers.base_controller import BaseController


class AreaController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, AreaModel)
    
    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()
        
        area: str = form.get('area')

        # Instanciar o objeto
        area_obj: AreaModel = AreaModel(area=area)
        
        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(area_obj)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            area_obj: AreaModel = await session.get(self.model, obj.id)

            if area_obj:
                # Recebe os dados do form
                form = await self.request.form()

                area: str = form.get('area')
               
                if area and area != area_obj.area:
                    area_obj.area = area
               
                await session.commit()

