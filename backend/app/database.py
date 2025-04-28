from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL")

#DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()  # Cria uma nova sessão com o banco
    try:
        yield db          # Entrega essa sessão para quem chamou (ex: uma rota)
    finally:
        db.close()        # Quando terminar de usar, fecha a sessão
