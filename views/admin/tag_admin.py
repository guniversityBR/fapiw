from datetime import datetime

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.tag_controller import TagController
from views.admin.base_crud_view import BaseCrudView



class TagAdmin(BaseCrudView):

    def __init__(self) -> None:
        super().__init__('tag')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos as tags [GET]
        """
        tag_controller: TagController = TagController(request)

        return await super().object_list(object_controller=tag_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar uma tag [DELETE]
        """
        tag_controller: TagController = TagController(request)

        tag_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=tag_controller, obj_id=tag_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        tag_controller: TagController = TagController(request)

        # Se o request for GET
        if request.method == 'GET':
            # Adicionar o request no context
            context = {"request": tag_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/tag/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await tag_controller.post_crud()
        except ValueError as err:
            tag: str = form.get('tag')
            dados = {"tag": tag}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/tag/create.html", context=context)
        
        return RedirectResponse(request.url_for("tag_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar uma tag [GET, POST]
        """
        tag_controller: TagController = TagController(request)

        tag_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET':
            return await super().object_details(object_controller=tag_controller, obj_id=tag_id)
        
        # Se o request for POST
        tag_obj = await tag_controller.get_one_crud(id_obj=tag_id)

        if not tag_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await tag_controller.put_crud(obj=tag_obj)
        except ValueError as err:
            tag: str = form.get('tag')
            dados = {"id": tag_id, "tag": tag}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "dados": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/tag/edit.html", context=context)
        
        return RedirectResponse(request.url_for("tag_list"), status_code=status.HTTP_302_FOUND)


tag_admin = TagAdmin()
