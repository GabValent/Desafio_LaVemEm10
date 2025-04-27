from sqlite3 import IntegrityError
from typing import List
from fastapi import APIRouter, Depends, HTTPException
import httpx
from app.Repository.onibusRepository import Onibus
from app.Repository.pontosRepository import Pontos
from app.DTO.onibusDTO import onibusBase
from sqlalchemy.orm import Session
from app.database import get_db
import redis
import json



router = APIRouter()
BASE_URL = "https://api.mobilidade.rio/gtfs"
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

@router.get("/busca")
async def buscar_paradas_da_linha(numero_linha: str, db: Session = Depends(get_db)):
    try:
        # Busca todas as paradas da linha solicitada, ordenadas pela sequência
        paradas = db.query(Pontos).filter(Pontos.linha == numero_linha).order_by(Pontos.sequencia).all()

        resultado = []
        for parada in paradas:
            resultado.append({
                "id": parada.id,   
                "nome": parada.nome,
                "lat": parada.lat,
                "lon": parada.lon,
                "sequencia": parada.sequencia
            })

        return resultado
    except Exception as e:
        print(f"Erro ao buscar paradas: {e}")
        raise

@router.get("/linhas", response_model=List[onibusBase])
def listar_linhas(db: Session = Depends(get_db)):
    return db.query(Onibus).all()


@router.get("/dados_onibus/{linha}")
def get_dados_onibus( linha: str):
    redis_key = f"linha:{linha}"
    dados_json = redis_client.get(redis_key)
    if dados_json:
        return json.loads(dados_json)
    return []



