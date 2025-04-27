from pydantic import BaseModel
from datetime import time
from typing import Optional

class ParadaBase(BaseModel):
    linha: str
    ponto: str
    janela_horario_inicio: time
    janela_horario_fim: time
    latitude: float
    longitude: float

class ParadaCreate(ParadaBase):
    usuario_id: int

    
class ParadaOutInterno(ParadaBase):
    id: int
    model_config = {
        "from_attributes": True
    }



class ParadaUpdate(BaseModel):
    linha: Optional[str] = None
    ponto: Optional[str] = None
    janela_horario_inicio: Optional[time] = None
    janela_horario_fim: Optional[time] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    model_config = {
        "from_attributes": True
    }
