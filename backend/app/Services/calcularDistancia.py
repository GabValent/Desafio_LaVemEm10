from datetime import datetime, timedelta
from app.database import SessionLocal
from app.Repository.paradaRepository import Parada
from app.celery_worker import celery
import requests
import os

headers = {
    "Content-Type": "application/json",
    "X-Application-Id": os.getenv("X_APPLICATION_ID"),
    "X-Api-Key": os.getenv("X_API_KEY")
}



def calcularDistancia(json, parada_id):
    # Iniciar a sessão do banco de dados uma vez
    db = SessionLocal()
    
    try:
        # Recuperar a parada do banco de dados
        parada = db.query(Parada).filter(Parada.id == parada_id).first()
        if not parada:
            raise ValueError(f"Parada com id {parada_id} não encontrada.")
        
        # Criar uma lista para armazenar as respostas
        respostas = []
        arrival_time = datetime.now().replace(microsecond=0).isoformat()
        for onibus in json:
            payload = {
                    "locations": [
                            {
                            "id": "Onibus",
                            "coords": {
                                "lat": onibus["latitude"],
                                "lng": onibus["longitude"]
                            }
                            },
                            {
                            "id": "Ponto",
                            "coords": {
                                "lat": parada.latitude,
                                "lng": parada.longitude
                            }
                            }
                    ],
                    "arrival_searches": [
                        {
                            "id": "Example Search",
                            "departure_location_ids": ["Onibus"],
                            "arrival_location_id": "Ponto", 
                            "transportation": { "type": "public_transport" },
                            "travel_time": 14400,  # Tempo de 4hrs, maximo da travelTime para pegar todos os onibus
                            "arrival_time": arrival_time,  
                            "arrival_time_period": "weekday_morning",
                            "properties": ["travel_time", "distance"]
                        }
                    ]
                }

            try:
                response_tt = requests.post("https://api.traveltimeapp.com/v4/time-filter", json=payload, headers=headers)

                if response_tt.status_code == 200:
                    data_tt = response_tt.json()
                    resultado = data_tt["results"][0]  # Pega o resultado
                    local = resultado["locations"][0]        # Pega o local
                    propriedades = local["properties"][0]    # Pega as propriedades

                    # Extraindo os valores
                    travel_time = propriedades["travel_time"]
                    distance = propriedades["distance"]
                    registro_onibus =  {
                        "ordem": onibus.get("ordem"),
                        "latitude": onibus["latitude"],
                        "longitude": onibus["longitude"],
                        "velocidade": onibus.get("velocidade"),
                        "linha": onibus.get("linha"),
                        "distancia": distance,
                        "tempo_chegada": travel_time
                    }
                    respostas.append(registro_onibus)
                else:
                    print(f"Erro na chamada TravelTime: {response_tt.status_code} - {response_tt.text}")
            except Exception as e:
                    print(f"Erro ao consultar TravelTime: {e}")
    
    finally:
        db.close() 

    return respostas
