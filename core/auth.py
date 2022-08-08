import hashlib
from typing import Optional

from fastapi import Response
from fastapi import Request
from passlib.handlers.sha2_crypt import sha512_crypt

from core.configs import settings

def try_hex_to_int(valor_hex: str) -> int:
    """
    Tenta converter e retornar um valor hexadecimal para inteiro ou devolve 0
    """
    try:
        return int(valor_hex, 16)
    except:
        return 0



def __gerar_hash_cookie(texto: str) -> str:
    """
    Função para gerar um hash de uma string para usar no cookie
    """
    texto = settings.SALTY + str(texto) + '__geek'
    return hashlib.sha512(texto.encode('utf-8')).hexdigest()



def set_auth(response: Response, membro_id: int) -> None:
    """
    Função que adiciona um cookie na response do usuário logado
    """
    valor_hash: str = __gerar_hash_cookie(str(membro_id))

    # Gerar o valor hexadecimal do membro_id e pega somente a parte que nos interessa
    membro_id_hex: str = hex(membro_id)[2:]

    # Montar o valor do token
    valor: str = membro_id_hex + '.' + valor_hash

    response.set_cookie(key=settings.AUTH_COOKIE_NAME, value=valor, httponly=True)


def gerar_hash_senha(senha: str) -> str:
    """
    Função que gera e retorna o hash de um texto/senha
    """
    hash_senha: str = sha512_crypt.hash(senha, rounds=123_456)

    return hash_senha


def verificar_senha(senha: str , hash_senha: str) -> bool:
    """
    Função que verifica se a senha é igual ao hash continido no banco de dados
    """
    return sha512_crypt.verify(secret=senha, hash=hash_senha)


def get_membro_id(request: Request) -> Optional[int]:
    """
    Recupera o membro_id do cookie
    """
    if settings.AUTH_COOKIE_NAME not in request.cookies:
        return None
    
    # Extrai o cookie
    valor = request.cookies[settings.AUTH_COOKIE_NAME]

    # Separa as partes através do ponto
    partes = valor.split('.')

    # pegar a parte correspondente ao membro_id
    membro_id_hex: str = partes[0]

    # Converte de hex para int
    membro_id_int: int = try_hex_to_int(membro_id_hex)

    # Gerar um hash para validar o hash do cookie
    check_valor_hash: str = __gerar_hash_cookie(membro_id_int)

    # adiciona o hex do membro_id e o ponto
    check_valor_hash = membro_id_hex + '.' + check_valor_hash
    
    # Validar o hash do cookie
    if valor != check_valor_hash:
        print('Alerta: Valor de cookie inválido.')
        return None
    
    return membro_id_int


def unset_auth(response: Response):
    """
    Função que remove o cookie do usuário da response
    """
    response.delete_cookie(settings.AUTH_COOKIE_NAME)

