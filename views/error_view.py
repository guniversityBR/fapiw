from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request

from core.configs import settings


async def not_found(request: Request, ext: HTTPException):
    """
    Retorna uma página 404
    """
    if 'admin' in str(request.url):
        template = 'admin/404.html'
    else:
        template = '404.html'
    
    context = {"request": request}

    return settings.TEMPLATES.TemplateResponse(template, context, status_code=status.HTTP_404_NOT_FOUND)


async def server_error(request: Request, ext: HTTPException):
    """
    Retorna uma página 500
    """
    if 'admin' in str(request.url):
        template = 'admin/500.html'
    else:
        template = '500.html'
    
    context = {"request": request}

    return settings.TEMPLATES.TemplateResponse(template, context, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


exception_handlers = {
    404: not_found,
    500: server_error
}


