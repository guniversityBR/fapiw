from typing import Optional, List

from fastapi.requests import Request
from sqlalchemy.future import select

from core.database import get_session
from models.tag_model import TagModel
from models.autor_model import AutorModel
from models.post_model import PostModel


class BaseController:

    def __init__(self, request: Request, model: object) -> None:
        self.request: Request = request
        self.model: object = model


    async def get_all_crud(self) -> Optional[List[object]]:
        """
        Retorna todos os registros do model
        """
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.scalars().unique().all()


    async def get_one_crud(self, id_obj: int) -> Optional[object]:
        """
        Retorna o objeto especificado pelo id_obj ou None
        """
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)

            return obj


    async def post_crud(self) -> None:
        raise NotImplementedError("Você precisa implementar este método.")


    async def put_crud(self, obj: object) -> None:
        raise NotImplementedError("Você precisa implementar este método.")
    
    
    async def del_crud(self, id_obj: int) -> None:
        async with get_session() as session:
            obj: self.model = await session.get(self.model, id_obj)

            if obj:
                await session.delete(obj)
                await session.commit()


    # Métodos genéricos

    async def get_objetos(self, model_obj: object) -> Optional[List[object]]:
        """
        Retorna todos os registros de object
        """
        async with get_session() as session:
            query = select(model_obj)
            result = await session.execute(query)
            objetos: Optional[List[model_obj]] = result.scalars().unique().all()

        return objetos
    

    async def get_objeto(self, model_obj: object, id_obj: int) -> Optional[object]:
        """
        Retorna o objeto especificado pelo id_obj ou None
        """
        async with get_session() as session:
            objeto: model_obj = await session.get(model_obj, id_obj)

        return objeto
