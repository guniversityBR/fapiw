from datetime import datetime

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.projeto_controller import ProjetoController
from views.admin.base_crud_view import BaseCrudView



class ProjetoAdmin(BaseCrudView):

    def __init__(self) -> None:
        super().__init__('projeto')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos os projetos [GET]
        """
        projeto_controller: ProjetoController = ProjetoController(request)

        return await super().object_list(object_controller=projeto_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar um projeto [DELETE]
        """
        projeto_controller: ProjetoController = ProjetoController(request)

        projeto_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=projeto_controller, obj_id=projeto_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        projeto_controller: ProjetoController = ProjetoController(request)

        # Se o request for GET
        if request.method == 'GET':
            # Adicionar o request no context
            context = {"request": projeto_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/projeto/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await projeto_controller.post_crud()
        except ValueError as err:
            titulo: str = form.get('titulo')
            descricao_inicial: str = form.get('descricao_inicial')
            descricao_final: str = form.get('descricao_final')
            dados = {"titulo": titulo, "descricao_inicial": descricao_inicial, "descricao_final": descricao_final}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/projeto/create.html", context=context)
        
        return RedirectResponse(request.url_for("projeto_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um projeto [GET, POST]
        """
        projeto_controller: ProjetoController = ProjetoController(request)

        projeto_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET':
            return await super().object_details(object_controller=projeto_controller, obj_id=projeto_id)
        
        # Se o request for POST
        projeto = await projeto_controller.get_one_crud(id_obj=projeto_id)

        if not projeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await projeto_controller.put_crud(obj=projeto)
        except ValueError as err:
            titulo: str = form.get('titulo')
            descricao_inicial: str = form.get('descricao_inicial')
            descricao_final: str = form.get('descricao_final')
            dados = {"id": projeto_id, "titulo": titulo, "descricao_inicial": descricao_inicial, "descricao_final": descricao_final}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "dados": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/projeto/edit.html", context=context)
        
        return RedirectResponse(request.url_for("projeto_list"), status_code=status.HTTP_302_FOUND)


projeto_admin = ProjetoAdmin()
