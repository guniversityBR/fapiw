from datetime import datetime
from typing import List

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.post_controller import PostController
from views.admin.base_crud_view import BaseCrudView
from models.autor_model import AutorModel
from models.tag_model import TagModel



class PostAdmin(BaseCrudView):

    def __init__(self) -> None:
        super().__init__('post')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos os posts [GET]
        """
        post_controller: PostController = PostController(request)

        return await super().object_list(object_controller=post_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar um post [DELETE]
        """
        post_controller: PostController = PostController(request)

        post_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=post_controller, obj_id=post_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        post_controller: PostController = PostController(request)

        # Se o request for GET
        if request.method == 'GET':
            # Adicionar o request, os autores e as tags no context
            autores = await post_controller.get_objetos(AutorModel)
            tags = await post_controller.get_objetos(TagModel)
            context = {"request": post_controller.request, "ano": datetime.now().year, "autores": autores, "tags": tags}

            return settings.TEMPLATES.TemplateResponse(f"admin/post/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await post_controller.post_crud()
        except ValueError as err:
            titulo: str = form.get('titulo')
            tags: List[object] = form.get('tags')
            texto: str = form.get('texto')
            autor: int = form.get('autor')
            dados = {"titulo": titulo, "tags": tags, "texto": texto, "autor": autor}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/post/create.html", context=context)
        
        return RedirectResponse(request.url_for("post_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um post [GET, POST]
        """
        post_controller: PostController = PostController(request)

        post_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET' and 'details' in str(post_controller.request.url):
            return await super().object_details(object_controller=post_controller, obj_id=post_id)
        
        elif request.method == 'GET' and 'edit' in str(post_controller.request.url):
            post = await post_controller.get_one_crud(id_obj=post_id)

            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Adicionar o request, os autores e as tags no context
            autores = await post_controller.get_objetos(AutorModel)
            tags = await post_controller.get_objetos(TagModel)
            context = {"request": post_controller.request, "ano": datetime.now().year, "objeto": post, "tags": tags, "autores": autores}

            return settings.TEMPLATES.TemplateResponse(f"admin/post/edit.html", context=context)
        
        # Se o request for POST
        post = await post_controller.get_one_crud(id_obj=post_id)

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await post_controller.put_crud(obj=post)
        except ValueError as err:
            titulo: str = form.get('titulo')
            tags: List[object] = form.get('tags')
            texto: str = form.get('texto')
            autor: int = form.get('autor')
            dados = {"id": post_id, "titulo": titulo, "tags": tags, "texto": texto, "autor": autor}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "dados": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/post/edit.html", context=context)
        
        return RedirectResponse(request.url_for("post_list"), status_code=status.HTTP_302_FOUND)


post_admin = PostAdmin()
