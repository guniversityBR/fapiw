from datetime import datetime

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.area_controller import AreaController
from views.admin.base_crud_view import BaseCrudView



class AreaAdmin(BaseCrudView):

    def __init__(self) -> None:
        super().__init__('area')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos as areas [GET]
        """
        area_controller: AreaController = AreaController(request)

        return await super().object_list(object_controller=area_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar uma area [DELETE]
        """
        area_controller: AreaController = AreaController(request)

        area_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=area_controller, obj_id=area_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        area_controller: AreaController = AreaController(request)

        # Se o request for GET
        if request.method == 'GET':
            # Adicionar o request no context
            context = {"request": area_controller.request, "ano": datetime.now().year}

            return settings.TEMPLATES.TemplateResponse(f"admin/area/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await area_controller.post_crud()
        except ValueError as err:
            area: str = form.get('area')
            dados = {"area": area}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "objeto": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/area/create.html", context=context)
        
        return RedirectResponse(request.url_for("area_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar uma area [GET, POST]
        """
        area_controller: AreaController = AreaController(request)

        area_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET':
            return await super().object_details(object_controller=area_controller, obj_id=area_id)
        
        # Se o request for POST
        area_obj = await area_controller.get_one_crud(id_obj=area_id)

        if not area_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await area_controller.put_crud(obj=area_obj)
        except ValueError as err:
            area: str = form.get('area')
            dados = {"id": area_id, "area": area}
            context = {
                "request": request,
                "ano": datetime.now().year,
                "error": err,
                "dados": dados
            }
            return settings.TEMPLATES.TemplateResponse("admin/area/edit.html", context=context)
        
        return RedirectResponse(request.url_for("area_list"), status_code=status.HTTP_302_FOUND)


area_admin = AreaAdmin()
