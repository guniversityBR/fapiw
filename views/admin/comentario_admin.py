from datetime import datetime

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.comentario_controller import ComentarioController
from views.admin.base_crud_view import BaseCrudView
from models.post_model import PostModel



class ComentarioAdmin(BaseCrudView):

    def __init__(self) -> None:   
        super().__init__('comentario')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos os comentários [GET]
        """
        comentario_controller: ComentarioController = ComentarioController(request)

        return await super().object_list(object_controller=comentario_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar um membro [DELETE]
        """
        comentario_controller: ComentarioController = ComentarioController(request)

        comentario_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=comentario_controller, obj_id=comentario_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        comentario_controller: ComentarioController = ComentarioController(request)

        # Se o request for GET
        if request.method == 'GET':
            # Adicionar o request e os posts no context
            posts = await comentario_controller.get_objetos(PostModel)
            context = {"request": comentario_controller.request, "ano": datetime.now().year, "posts": posts}

            return settings.TEMPLATES.TemplateResponse(f"admin/comentario/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await comentario_controller.post_crud()
        except ValueError as err:
            id_post: int = form.get('post')
            autor: str = form.get('autor')
            texto: str = form.get('texto')
            posts = await comentario_controller.get_objetos(PostModel)
            dados = {"id_post": id_post, "autor": autor, "texto": texto}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "posts": posts,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/comentario/create.html", context=context)
        
        return RedirectResponse(request.url_for("comentario_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um comentário [GET, POST]
        """
        comentario_controller: ComentarioController = ComentarioController(request)

        comentario_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET'  and 'details' in str(comentario_controller.request.url):
            return await super().object_details(object_controller=comentario_controller, obj_id=comentario_id)
        
        elif request.method == 'GET' and 'edit' in str(comentario_controller.request.url):
            comentario = await comentario_controller.get_one_crud(id_obj=comentario_id)

            if not comentario:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Adicionar o request e os posts no context
            posts = await comentario_controller.get_objetos(PostModel)
            context = {"request": comentario_controller.request, "ano": datetime.now().year, "objeto": comentario, "posts": posts}

            return settings.TEMPLATES.TemplateResponse(f"admin/comentario/edit.html", context=context)
        
        # Se o request for POST
        comentario = await comentario_controller.get_one_crud(id_obj=comentario_id)

        if not comentario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await comentario_controller.put_crud(obj=comentario)
        except ValueError as err:
            post: int = form.get('post')
            autor: str = form.get('autor')
            texto: str = form.get('texto')
            dados = {"id": comentario_id, "post": post, "autor": autor, "texto": texto}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "dados": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/comentario/edit.html", context=context)
        
        return RedirectResponse(request.url_for("comentario_list"), status_code=status.HTTP_302_FOUND)


comentario_admin = ComentarioAdmin()
