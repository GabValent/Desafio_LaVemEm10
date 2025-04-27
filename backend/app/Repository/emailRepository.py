from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class EmailRegistro(Base):
    __tablename__ = "email_registro"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    linha = Column(String, nullable=False)
    horario = Column(DateTime, default=datetime.utcnow, nullable=False)
    enviado = Column(Boolean, default=False, nullable=False)  # Flag para saber se foi enviado ou não

    usuario = relationship("Usuario", back_populates="email_registros")
