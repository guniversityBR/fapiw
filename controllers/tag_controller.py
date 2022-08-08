from fastapi.requests import Request

from core.database import get_session
from models.tag_model import TagModel
from controllers.base_controller import BaseController


class TagController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, TagModel)
    
    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()
        
        tag: str = form.get('tag')

        # Instanciar o objeto
        tag_obj: TagModel = TagModel(tag=tag)
        
        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(tag_obj)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            tag_obj: TagModel = await session.get(self.model, obj.id)

            if tag_obj:
                # Recebe os dados do form
                form = await self.request.form()

                tag: str = form.get('tag')

                if tag and tag != tag_obj.tag:
                    tag_obj.tag = tag
        
                await session.commit()

