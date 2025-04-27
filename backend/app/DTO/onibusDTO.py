from pydantic import BaseModel


class onibusBase(BaseModel):
    numero_linha: str
    nome_linha: str