import pytest
from app.Services.filtrarLinha import filtrar_onibus_por_linha

def test_filtrar_onibus_por_linha():
    response_json = [
        {"ordem": "B25523", "linha": "232", "latitude": "-22,90641", "longitude": "-43,17595", "velocidade": "0", "datahoraenvio": "1744117271000"},
        {"ordem": "B25587", "linha": "606", "latitude": "-22,89986", "longitude": "-43,21122", "velocidade": "1", "datahoraenvio": "1744117271000"},
        {"ordem": "B25606", "linha": "232", "latitude": "-22,90436", "longitude": "-43,2953", "velocidade": "32", "datahoraenvio": "1744117271000"}
    ]
    linha = "232"
    
    resultado = filtrar_onibus_por_linha(response_json, linha)

    # Verifica se o número de ônibus filtrados está correto
    assert len(resultado) == 2

    # Verifica se todos os ônibus filtrados possuem a linha correta
    for onibus in resultado:
        assert onibus["linha"] == "232"

    # Verifica se os dados dos ônibus estão corretos (ordem, latitude, longitude)
    assert resultado[0]["ordem"] == "B25523"
    assert resultado[1]["ordem"] == "B25606"
    assert resultado[0]["latitude"] == -22.90641
    assert resultado[0]["longitude"] == -43.17595
    assert resultado[1]["latitude"] == -22.90436
    assert resultado[1]["longitude"] == -43.2953

    # Verifica se a datahoraenvio está sendo corretamente tratada como timestamp
    assert resultado[0]["datahoraenvio"] == 1744117271000
    assert resultado[1]["datahoraenvio"] == 1744117271000
