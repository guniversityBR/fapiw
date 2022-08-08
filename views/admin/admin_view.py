from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi import status

from core.configs import settings
from views.admin.membro_admin import membro_admin
from views.admin.area_admin import area_admin
from views.admin.autor_admin import autor_admin
from views.admin.comentario_admin import comentario_admin
from views.admin.duvida_admin import duvida_admin
from views.admin.post_admin import post_admin
from views.admin.projeto_admin import projeto_admin
from views.admin.tag_admin import tag_admin
from core.deps import valida_login

router = APIRouter(prefix="/admin")
router.include_router(membro_admin.router)
router.include_router(area_admin.router)
router.include_router(autor_admin.router)
router.include_router(comentario_admin.router)
router.include_router(duvida_admin.router)
router.include_router(post_admin.router)
router.include_router(projeto_admin.router)
router.include_router(tag_admin.router)


@router.get('/', name='admin_index')
async def admin_index(request: Request):
    context = await valida_login(request)

    try:
        if not context["membro"]:
            return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
    except KeyError:
        return settings.TEMPLATES.TemplateResponse('admin/limbo.html', context=context, status_code=status.HTTP_404_NOT_FOUND)
    
    return settings.TEMPLATES.TemplateResponse('admin/index.html', context=context)

