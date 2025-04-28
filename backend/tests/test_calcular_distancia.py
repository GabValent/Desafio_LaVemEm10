import pytest
from unittest.mock import patch, MagicMock
from app.Services.calcularDistancia import calcularDistancia
from app.Repository.paradaRepository import Parada

@patch("app.Services.calcularDistancia.requests.post")
@patch("app.Services.calcularDistancia.SessionLocal")
def test_calcular_distancia_mockado(mock_session, mock_post):
    # Mock do banco de dados
    mock_db_instance = MagicMock()
    mock_session.return_value = mock_db_instance
    
    mock_parada = MagicMock(spec=Parada)
    mock_parada.id = 1
    mock_parada.latitude = -22.9068
    mock_parada.longitude = -43.1729
    mock_db_instance.query.return_value.filter.return_value.first.return_value = mock_parada
    
    # Simulando a resposta do `requests.post`
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "results": [{
            "locations": [{
                "properties": [{
                    "travel_time": 300,
                    "distance": 1000
                }]
            }]
        }]
    }
    
    json_onibus = [{
        "ordem": 1,
        "latitude": -22.9068,
        "longitude": -43.1729,
        "velocidade": 50,
        "linha": "10",
        "datahoraenvio": "2025-04-28T10:00:00"
    }]
    parada_id = 1
    
    resultado = calcularDistancia(json_onibus, parada_id)
    
    # Verificando o resultado
    assert len(resultado) == 1
    assert resultado[0]["distancia"] == 1000
    assert resultado[0]["tempo_chegada"] == 300
    
    # Testando comportamento quando a parada não é encontrada
    mock_db_instance.query.return_value.filter.return_value.first.return_value = None
    resultado_vazio = calcularDistancia(json_onibus, parada_id)
    assert resultado_vazio == []

    # Testando quando a resposta da TravelTime não é 200
    mock_post.return_value.status_code = 500
    resultado_erro = calcularDistancia(json_onibus, parada_id)
    assert resultado_erro == []
