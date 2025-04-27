from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    login: str
    email: str

class UsuarioCreate(UsuarioBase):
    senha: str
    
class UsuarioOutInterno(BaseModel):
    id: int
    login: str
    email: str
    
   
    model_config = {
        "from_attributes": True  
    }

class UsuarioLogin(BaseModel):
    login: str
    senha: str

class UsuarioUpdate(BaseModel):
    login: Optional[str] = None
    senha: Optional[str] = None
    email: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
