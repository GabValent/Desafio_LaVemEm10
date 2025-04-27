def filtrar_onibus_por_linha(response_json, linha):
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
           
            if ordem not in onibus_por_ordem or datahoraenvio > onibus_por_ordem[ordem]["datahoraenvio"]:
                onibus_filtrado = {
                    "ordem": ordem,
                    "latitude": float(onibus["latitude"].replace(",", ".")) if onibus.get("latitude") else None,
                    "longitude": float(onibus["longitude"].replace(",", ".")) if onibus.get("longitude") else None,
                    "velocidade": onibus.get("velocidade"),
                    "linha": onibus.get("linha"),
                    "datahoraenvio": datahoraenvio
                }
                onibus_por_ordem[ordem] = onibus_filtrado

    return list(onibus_por_ordem.values())
