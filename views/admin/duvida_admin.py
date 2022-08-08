from datetime import datetime

from fastapi.routing import APIRouter
from starlette.routing import Route
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.duvida_controller import DuvidaController
from views.admin.base_crud_view import BaseCrudView
from models.area_model import AreaModel



class DuvidaAdmin(BaseCrudView):

    def __init__(self) -> None:
        super().__init__('duvida')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos as dúvidas [GET]
        """
        duvida_controller: DuvidaController = DuvidaController(request)

        return await super().object_list(object_controller=duvida_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar uma dúvida [DELETE]
        """
        duvida_controller: DuvidaController = DuvidaController(request)

        duvida_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=duvida_controller, obj_id=duvida_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        duvida_controller: DuvidaController = DuvidaController(request)

        # Se o request for GET
        if request.method == 'GET':
            # Adicionar o request e as áreas no context
            areas = await duvida_controller.get_objetos(AreaModel)
            context = {"request": duvida_controller.request, "ano": datetime.now().year, "areas": areas}

            return settings.TEMPLATES.TemplateResponse(f"admin/duvida/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await duvida_controller.post_crud()
        except ValueError as err:
            area: int = form.get('area')
            titulo: str = form.get('titulo')
            resposta: str = form.get('resposta')
            dados = {"area": area, "titulo": titulo, "resposta": resposta}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/duvida/create.html", context=context)
        
        return RedirectResponse(request.url_for("duvida_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar uma dúvida [GET, POST]
        """
        duvida_controller: DuvidaController = DuvidaController(request)

        duvida_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET' and 'details' in str(duvida_controller.request.url):
            return await super().object_details(object_controller=duvida_controller, obj_id=duvida_id)

        elif request.method == 'GET' and 'edit' in str(duvida_controller.request.url):
            duvida = await duvida_controller.get_one_crud(id_obj=duvida_id)

            if not duvida:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
            
            # Adicionar o request e as áreas no context
            areas = await duvida_controller.get_objetos(AreaModel)
            context = {"request": duvida_controller.request, "ano": datetime.now().year, "objeto": duvida, "areas": areas}

            return settings.TEMPLATES.TemplateResponse(f"admin/duvida/edit.html", context=context)
        
        # Se o request for POST
        duvida = await duvida_controller.get_one_crud(id_obj=duvida_id)

        if not duvida:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await duvida_controller.put_crud(obj=duvida)
        except ValueError as err:
            area_id: int = form.get('area')
            titulo: str = form.get('titulo')
            resposta: str = form.get('resposta')
            dados = {"id": duvida_id, "area": area_id, "titulo": titulo, "resposta": resposta}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "dados": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/duvida/edit.html", context=context)
        
        return RedirectResponse(request.url_for("duvida_list"), status_code=status.HTTP_302_FOUND)


duvida_admin = DuvidaAdmin()
