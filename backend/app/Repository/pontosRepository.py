from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import validates
from app.database import Base

class Pontos(Base):
    __tablename__ = "Pontos"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID auto-incrementado pelo banco
    nome = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    sequencia = Column(Integer, nullable=False)
    linha = Column(String, nullable=False)
    stop_id = Column(String, nullable=False)  # Este campo será apenas informativo, não será chave primária
