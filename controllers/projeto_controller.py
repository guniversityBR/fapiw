from fastapi.requests import Request
from fastapi import UploadFile

from aiofile import async_open

from uuid import uuid4

from core.configs import settings
from core.database import get_session
from models.projeto_model import ProjetoModel
from controllers.base_controller import BaseController


class ProjetoController(BaseController):

    def __init__(self, request: Request) -> None:
        super().__init__(request, ProjetoModel)
    
    async def post_crud(self) -> None:
        # Recebe dados do form
        form = await self.request.form()
        
        titulo: str = form.get('titulo')
        descricao_inicial: str = form.get('descricao_inicial')
        imagem1: UploadFile = form.get('imagem1')
        imagem2: UploadFile = form.get('imagem2')
        imagem3: UploadFile = form.get('imagem3')
        descricao_final: str = form.get('descricao_final')

        # Nome aleatório para a imagem1
        arquivo_ext1: str = imagem1.filename.split('.')[-1]
        novo_nome1: str = f"{str(uuid4())}.{arquivo_ext1}"

        # Nome aleatório para a imagem2
        arquivo_ext2: str = imagem2.filename.split('.')[-1]
        novo_nome2: str = f"{str(uuid4())}.{arquivo_ext2}"

        # Nome aleatório para a imagem3
        arquivo_ext3: str = imagem3.filename.split('.')[-1]
        novo_nome3: str = f"{str(uuid4())}.{arquivo_ext3}"

        # Instanciar o objeto
        projeto: ProjetoModel = ProjetoModel(titulo=titulo, descricao_inicial=descricao_inicial, imagem1=novo_nome1, imagem2=novo_nome2, imagem3=novo_nome3, descricao_final=descricao_final)

        # Fazer o upload do arquivo1
        async with async_open(f"{settings.MEDIA}/projeto/{novo_nome1}", "wb") as afile:
            await afile.write(imagem1.file.read())
        
        # Fazer o upload do arquivo2
        async with async_open(f"{settings.MEDIA}/projeto/{novo_nome2}", "wb") as afile:
            await afile.write(imagem2.file.read())

        # Fazer o upload do arquivo3
        async with async_open(f"{settings.MEDIA}/projeto/{novo_nome3}", "wb") as afile:
            await afile.write(imagem3.file.read())
        
        # Cria a sessão e insere no banco de dados
        async with get_session() as session:
            session.add(projeto)
            await session.commit()
 

    async def put_crud(self, obj: object) -> None:
        async with get_session() as session:
            projeto: ProjetoModel = await session.get(self.model, obj.id)

            if projeto:
                # Recebe os dados do form
                form = await self.request.form()

                titulo: str = form.get('titulo')
                descricao_inicial: str = form.get('descricao_inicial')
                imagem1: UploadFile = form.get('imagem1')
                imagem2: UploadFile = form.get('imagem2')
                imagem3: UploadFile = form.get('imagem3')
                descricao_final: str = form.get('descricao_final')

                if titulo and titulo != projeto.titulo:
                    projeto.titulo = titulo

                if descricao_inicial and descricao_inicial != projeto.descricao_inicial:
                    projeto.descricao_inicial = descricao_inicial

                if imagem1.filename:
                    # Gera um nome aleatório para imagem1
                    arquivo_ext1: str = imagem1.filename.split('.')[-1]
                    novo_nome1: str = f"{str(uuid4())}.{arquivo_ext1}"
                    projeto.imagem1 = novo_nome1
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/projeto/{novo_nome1}", "wb") as afile:
                        await afile.write(imagem1.file.read())

                if imagem2.filename:
                    # Gera um nome aleatório para imagem2
                    arquivo_ext2: str = imagem2.filename.split('.')[-1]
                    novo_nome2: str = f"{str(uuid4())}.{arquivo_ext2}"
                    projeto.imagem2 = novo_nome2
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/projeto/{novo_nome2}", "wb") as afile:
                        await afile.write(imagem2.file.read())

                if imagem3.filename:
                    # Gera um nome aleatório para imagem1
                    arquivo_ext3: str = imagem3.filename.split('.')[-1]
                    novo_nome3: str = f"{str(uuid4())}.{arquivo_ext3}"
                    projeto.imagem3 = novo_nome3
                    # Faz o upload da imagem
                    async with async_open(f"{settings.MEDIA}/projeto/{novo_nome3}", "wb") as afile:
                        await afile.write(imagem3.file.read())

                if descricao_final and descricao_final != projeto.descricao_final:
                    projeto.descricao_final = descricao_final
                    
                await session.commit()

