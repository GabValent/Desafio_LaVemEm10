import logging
from fastapi import FastAPI
from app.Resource import onibusAPI, paradaAPI, usuarioAPI
from app.database import Base, engine
from app.Repository.emailRepository import EmailRegistro
from app.Repository.onibusRepository import Onibus
from app.Repository.pontosRepository import Pontos
from .pontos import buscar_pontos
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Instanciando o FastAPI
app = FastAPI()

# Configuração do CORS
origins = [
    "http://localhost:3000",
    "*", 
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # permite todos os métodos: GET, POST, OPTIONS, etc.
    allow_headers=["*"],  # permite todos os headers
)

# Registrando as rotas
app.include_router(onibusAPI.router, prefix="/onibus", tags=["onibus"])
app.include_router(usuarioAPI.router, prefix="/usuarios", tags=["usuarios"])
app.include_router(paradaAPI.router, prefix="/paradas", tags=["paradas"])

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




#Tirar o comentario quando quiser atualizar os pontos

'''
@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando a busca de pontos...")
    try:
        await buscar_pontos()
        logger.info("Busca de pontos finalizada com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao buscar pontos: {e}")

'''

