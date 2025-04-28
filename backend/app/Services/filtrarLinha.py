import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def filtrar_onibus_por_linha(response_json: List[Dict[str, Any]], linha: str) -> List[Dict[str, Any]]:
    """
    Filtra os ônibus da resposta JSON pela linha fornecida e converte
    as coordenadas de latitude e longitude para float, adequando ao formato da TravelTime API.

    :param response_json: A lista de dados JSON que contém as informações dos ônibus.
    :param linha: O número da linha do ônibus que deve ser filtrado.
    :return: Uma lista de ônibus que correspondem à linha fornecida, com as coordenadas em formato float.
    """
    onibus_por_ordem = {}

    for onibus in response_json:
        if onibus.get("linha") == linha:
            ordem = onibus.get("ordem")
            datahoraenvio = int(onibus.get("datahoraenvio", 0))

            # Se já temos o ônibus e o novo é mais recente, substituímos
            if ordem not in onibus_por_ordem or datahoraenvio > onibus_por_ordem[ordem]["datahoraenvio"]:
                try:
                    latitude_str = onibus.get("latitude")
                    longitude_str = onibus.get("longitude")
                    
                    latitude = float(latitude_str.replace(",", ".")) if isinstance(latitude_str, str) else None
                    longitude = float(longitude_str.replace(",", ".")) if isinstance(longitude_str, str) else None

                    onibus_filtrado = {
                        "ordem": ordem,
                        "latitude": latitude,
                        "longitude": longitude,
                        "velocidade": onibus.get("velocidade"),
                        "linha": onibus.get("linha"),
                        "datahoraenvio": datahoraenvio
                    }
                    onibus_por_ordem[ordem] = onibus_filtrado

                except (ValueError, AttributeError) as e:
                    logger.warning(f"Erro ao processar ônibus {ordem}: {e}")

    return list(onibus_por_ordem.values())
