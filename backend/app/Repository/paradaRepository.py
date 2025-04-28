from sqlalchemy import Column, Integer, String, Time, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Parada(Base):
    __tablename__ = "paradas"

    id = Column(Integer, primary_key=True, index=True)
    linha = Column(String, nullable=False)
    ponto = Column(String, nullable=False)
    janela_horario_inicio = Column(Time, nullable=False)
    janela_horario_fim = Column(Time, nullable=False)  
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    latitude = Column(Float, nullable=False )
    longitude = Column(Float, nullable=False )


    def get_id(self) -> int:
        return self.id

    def set_id(self, id_: int):
        self.id = id_

    def get_linha(self) -> str:
        return self.linha

    def set_linha(self, linha: str):
        self.linha = linha

    def get_ponto(self) -> str:
        return self.ponto

    def set_ponto(self, ponto: str):
        self.ponto = ponto

    def get_janela_horario_inicio(self) -> Time:
        return self.janela_horario_inicio

    def set_janela_horario_inicio(self, horario: Time):
        self.janela_horario_inicio = horario

    def get_janela_horario_fim(self) -> Time:
        return self.janela_horario_fim

    def set_janela_horario_fim(self, horario: Time):
        self.janela_horario_fim = horario

    def get_usuario_id(self) -> int:
        return self.usuario_id

    def set_usuario_id(self, usuario_id: int):
        self.usuario_id = usuario_id

    def get_latitude(self) -> float:
        return self.latitude

    def set_latitude(self, latitude: float):
        self.latitude = latitude

    def get_longitude(self) -> float:
        return self.longitude

    def set_longitude(self, longitude: float):
        self.longitude = longitude
    


    usuario = relationship("Usuario", back_populates="paradas")
