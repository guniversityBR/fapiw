from fastapi.routing import APIRouter
from fastapi.routing import APIRoute
from fastapi import status
from fastapi.responses import Response
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.base_controller import BaseController
from core.deps import valida_login


class BaseCrudView:

    def __init__(self, template_base: str) -> None:
        self.template_base: str = template_base

        self.router = APIRouter()
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/list", endpoint=self.object_list, methods=["GET",], name=f'{self.template_base}_list'))
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/create", endpoint=self.object_create, methods=["GET", "POST"], name=f'{self.template_base}_create'))
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/details/"+'{obj_id:int}', endpoint=self.object_edit, methods=["GET",], name=f'{self.template_base}_details'))
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/edit/"+'{obj_id:int}', endpoint=self.object_edit, methods=["GET", "POST"], name=f'{self.template_base}_edit'))
        self.router.routes.append(APIRoute(path=f"/{self.template_base}/delete/"+'{obj_id:int}', endpoint=self.object_delete, methods=["DELETE",], name=f'{self.template_base}_delete'))


    async def object_create(self) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        raise NotImplementedError("Você precisa implementar este método.")


    async def object_edit(self) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um objeto [GET, POST]
        """
        raise NotImplementedError("Você precisa implementar este método.")
     

    async def object_list(self, object_controller: BaseController) -> Response:
        """
        Rota para listar todos os objetos [GET]
        """
        context = await valida_login(object_controller.request)

        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        dados = await object_controller.get_all_crud()

        context.update({"dados": dados})

        return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/list.html", context=context)


    async def object_delete(self, object_controller: BaseController, obj_id: int) -> Response:
        """
        Rota para deletar um objeto [DELETE]
        """
        context = await valida_login(object_controller.request)

        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        objeto = await object_controller.get_one_crud(id_obj=obj_id)

        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        await object_controller.del_crud(id_obj=objeto.id)


        return Response(object_controller.request.url_for(f"{self.template_base}_list"))


    async def object_details(self, object_controller: BaseController, obj_id: int) -> Response:
        """
        Rota para apresentar os detalhes de um objeto [GET]
        """
        context = await valida_login(object_controller.request)

        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        objeto = await object_controller.get_one_crud(id_obj=obj_id)

        if not objeto:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        context.update({"objeto": objeto})

        if 'details' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/details.html", context=context)
        
        elif 'edit' in str(object_controller.request.url):
            return settings.TEMPLATES.TemplateResponse(f"admin/{self.template_base}/edit.html", context=context)
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

