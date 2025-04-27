from sqlalchemy import Column, Integer, String
from app.database import Base

class Onibus(Base):
    __tablename__ = "onibus"

    id = Column(Integer, primary_key=True, index=True)
    numero_linha = Column(String, index=True)
    nome_linha = Column(String)
