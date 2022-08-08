from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response, RedirectResponse
from fastapi.exceptions import HTTPException

from core.configs import settings
from controllers.membro_controller import MembroController
from views.admin.base_crud_view import BaseCrudView
from core.deps import valida_login



class MembroAdmin(BaseCrudView):

    def __init__(self) -> None: 
        super().__init__('membro')
    

    async def object_list(self, request: Request) -> Response:
        """
        Rota para listar todos os membros [GET]
        """
        membro_controller: MembroController = MembroController(request)

        return await super().object_list(object_controller=membro_controller)


    async def object_delete(self, request: Request) -> Response:
        """
        Rota para deletar um membro [DELETE]
        """
        membro_controller: MembroController = MembroController(request)

        membro_id: int = request.path_params["obj_id"]

        return await super().object_delete(object_controller=membro_controller, obj_id=membro_id)
    

    async def object_create(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário e criar um objeto [GET, POST]
        """
        context = await valida_login(request)

        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        membro_controller: MembroController = MembroController(request)

        # Se o request for GET
        if request.method == 'GET':
            return settings.TEMPLATES.TemplateResponse(f"admin/membro/create.html", context=context)
        
        # Se o request for POST
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await membro_controller.post_crud()
        except ValueError as err:
            nome: str = form.get('nome')
            funcao: str = form.get('funcao')
            email: str = form.get('email')
            senha: str = form.get('senha')
            dados = {"nome": nome, "funcao": funcao, "email": email, "senha": senha}
            context.update({"error": err,"objeto": dados})
            return settings.TEMPLATES.TemplateResponse("admin/membro/create.html", context=context)
        
        return RedirectResponse(request.url_for("membro_list"), status_code=status.HTTP_302_FOUND)

    
    async def object_edit(self, request: Request) -> Response:
        """
        Rota para carregar o template do formulário de edição e atualizar um membro [GET, POST]
        """
        context = await valida_login(request)

        try:
           if not context["membro"]:
               return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)

        membro_controller: MembroController = MembroController(request)

        membro_id: int = request.path_params["obj_id"]
        
        # Se o request for GET
        if request.method == 'GET':
            return await super().object_details(object_controller=membro_controller, obj_id=membro_id)
        
        # Se o request for POST
        membro = await membro_controller.get_one_crud(id_obj=membro_id)

        if not membro:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        # Recebe os dados do form
        form = await request.form()
        dados: set = None

        try:
            await membro_controller.put_crud(obj=membro)
        except ValueError as err:
            nome: str = form.get('nome')
            funcao: str = form.get('funcao')
            email: str = form.get('email')
            senha: str = form.get('senha')
            dados = {"id": membro_id, "nome": nome, "funcao": funcao, "email": email, "senha": senha}
            context.update({"error": err,"dados": dados})
            return settings.TEMPLATES.TemplateResponse("admin/membro/edit.html", context=context)
        
        return RedirectResponse(request.url_for("membro_list"), status_code=status.HTTP_302_FOUND)


membro_admin = MembroAdmin()
