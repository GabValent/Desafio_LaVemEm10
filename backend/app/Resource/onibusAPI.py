import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import redis
import json

from app.Repository.onibusRepository import Onibus
from app.Repository.pontosRepository import Pontos
from app.DTO.onibusDTO import onibusBase
from app.database import get_db

# Configura o logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()
BASE_URL = "https://api.mobilidade.rio/gtfs"
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@router.get("/busca")
async def buscar_paradas_da_linha(numero_linha: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando paradas da linha {numero_linha}")
        paradas = db.query(Pontos).filter(Pontos.linha == numero_linha).order_by(Pontos.sequencia).all()

        resultado = [{
            "id": parada.id,
            "nome": parada.nome,
            "lat": parada.lat,
            "lon": parada.lon,
            "sequencia": parada.sequencia
        } for parada in paradas]

        return resultado

    except Exception as e:
        logger.error(f"Erro ao buscar paradas da linha {numero_linha}: {e}")
        raise HTTPException(status_code=500, detail="Erro ao buscar paradas.")

@router.get("/linhas", response_model=List[onibusBase])
def listar_linhas(db: Session = Depends(get_db)):
    logger.info("Listando linhas disponíveis.")
    return db.query(Onibus).all()

@router.get("/dados_onibus/{linha}")
def get_dados_onibus(linha: str):
    logger.info(f"Consultando dados de ônibus da linha {linha} no Redis.")
    redis_key = f"linha:{linha}"
    dados_json = redis_client.get(redis_key)
    if dados_json:
        logger.info(f"Dados encontrados para linha {linha}.")
        return json.loads(dados_json)
    logger.warning(f"Nenhum dado encontrado no Redis para a linha {linha}.")
    return []
