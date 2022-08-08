from typing import List, Optional

from sqlalchemy.future import select
from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.autor_model import AutorModel
from controllers.base_controller import BaseController
from models.tag_model import TagModel


class AutorController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, AutorModel)


    async def get_all_crud(self) -> Optional[List[AutorModel]]:
        """
        Retorna todos os registros do model
        """
        async with get_session() as session:
            query = select(self.model)
            result = await session.execute(query)

            return result.scalars().unique().all()
    

    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()
        
        nome: str = form.get('nome')
        imagem: UploadFile = form.get('imagem')
        tags: List[str] = form.getlist('tag')

        # Nome aleatório para a imagem
        arquivo_ext: str = imagem.filename.split('.')[-1]
        novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"

        # Instanciar o objeto
        autor: AutorModel = AutorModel(nome=nome, imagem=novo_nome)

        # Busca e adiciona as tags
        for id_tag in tags:
            tag = await self.get_objeto(model_obj=TagModel, id_obj=int(id_tag))
            autor.tags.append(tag)

        # Fazer o upload do arquivo
        async with async_open(f"{settings.MEDIA}/autor/{novo_nome}", "wb") as afile:
            await afile.write(imagem.file.read())
        
        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(autor)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            autor: AutorModel = await session.get(self.model, obj.id)

            if autor:
                # Recebe os dados do form
                form = await self.request.form()

                nome: str = form.get('nome')
                imagem: UploadFile = form.get('imagem')
                tags: List[str] = form.getlist('tag')

                if nome and nome != autor.nome:
                    autor.nome = nome
                if tags:
                    # Se houver tags, zeramos as presentes no autor
                    autor.tags = []
                    await session.commit()
                    # Busca e adiciona as tags
                    for id_tag in tags:
                        tag = await self.get_objeto(model_obj=TagModel, id_obj=int(id_tag))
                        # Operação para juntar o objeto tag que vem de outra
                        # sessão com o objeto autor que está nesta sessão.
                        tag_local = await session.merge(tag)
                        autor.tags.append(tag_local)
                if imagem.filename:
                    # Gera um nome aleatório
                    arquivo_ext: str = imagem.filename.split('.')[-1]
                    novo_nome: str = f"{str(uuid4())}.{arquivo_ext}"
                    autor.imagem = novo_nome
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/autor/{novo_nome}", "wb") as afile:
                        await afile.write(imagem.file.read())
                await session.commit()

