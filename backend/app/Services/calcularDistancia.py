import logging
from datetime import datetime
import requests
import os
from app.database import SessionLocal
from app.Repository.paradaRepository import Parada


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


headers = {
    "Content-Type": "application/json",
    "X-Application-Id": os.getenv("X_APPLICATION_ID"),
    "X-Api-Key": os.getenv("X_API_KEY")
}

def calcularDistancia(json_onibus, parada_id):
    db = SessionLocal()

    try:
        # Recuperar a parada do banco de dados
        parada = db.query(Parada).filter(Parada.id == parada_id).first()
        if not parada:
            logger.warning(f"Parada com id {parada_id} não encontrada.")
            return []

        respostas = []
        arrival_time = datetime.now().replace(microsecond=0).isoformat()

        for onibus in json_onibus:
            payload = {
                "locations": [
                    {"id": "Onibus", "coords": {"lat": onibus["latitude"], "lng": onibus["longitude"]}},
                    {"id": "Ponto", "coords": {"lat": parada.latitude, "lng": parada.longitude}}
                ],
                "arrival_searches": [
                    {
                        "id": "Example Search",
                        "departure_location_ids": ["Onibus"],
                        "arrival_location_id": "Ponto",
                        "transportation": {"type": "public_transport"},
                        "travel_time": 14400,  # 4 horas, limite da TravelTime
                        "arrival_time": arrival_time,
                        "arrival_time_period": "weekday_morning",
                        "properties": ["travel_time", "distance"]
                    }
                ]
            }

            try:
                response_tt = requests.post(
                    "https://api.traveltimeapp.com/v4/time-filter",
                    json=payload,
                    headers=headers
                )

                if response_tt.status_code == 200:
                    data_tt = response_tt.json()
                    resultado = data_tt["results"][0] # Pega o resultado
                    local = resultado["locations"][0] # Pega o local
                    propriedades = local["properties"][0] # Pega as propriedades

                    travel_time = propriedades.get("travel_time")
                    distance = propriedades.get("distance")

                    registro_onibus = {
                        "ordem": onibus.get("ordem"),
                        "latitude": onibus.get("latitude"),
                        "longitude": onibus.get("longitude"),
                        "velocidade": onibus.get("velocidade"),
                        "linha": onibus.get("linha"),
                        "distancia": distance,
                        "tempo_chegada": travel_time
                    }
                    respostas.append(registro_onibus)
                else:
                    logger.error(f"Erro TravelTime {response_tt.status_code}: {response_tt.text}")

            except requests.RequestException as e:
                logger.exception(f"Erro ao consultar TravelTime para ônibus {onibus.get('ordem')}: {e}")

    finally:
        db.close()

    return respostas
