from typing import TypedDict

class UserType(TypedDict):
    id: int
    nome: str 
    email: str 
    telefone: str 
    permissao: str 
    senha: str