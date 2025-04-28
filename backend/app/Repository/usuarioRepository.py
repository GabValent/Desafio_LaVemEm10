from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True, nullable=False)
    senha = Column(String, nullable=False)
    email = Column(String,unique = True, nullable=False)


    def get_id(self) -> int:
        return self.id
    
    def get_login(self) -> str:
        return self.login

    def set_senha(self, nova_senha: str):
        self.senha = nova_senha

    def set_email(self, novo_email: str):
        self.email = novo_email

    paradas = relationship("Parada", back_populates="usuario")
    email_registros = relationship("EmailRegistro", back_populates="usuario", lazy = 'select')