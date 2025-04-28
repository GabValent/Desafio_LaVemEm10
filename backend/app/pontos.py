import httpx
from app.database import SessionLocal
from app.Repository.pontosRepository import Pontos
from sqlalchemy.exc import IntegrityError
from app.Repository.onibusRepository import Onibus

url_pontos = "https://api.mobilidade.rio/gtfs"
url_onibus = "https://api.mobilidade.rio/gtfs/routes/"

async def buscar_pontos():
    session = SessionLocal()

    try:
        total_pages = 1483  # Número total de páginas a serem buscadas

        async with httpx.AsyncClient(timeout=300) as client:
            for page_number in range(1, total_pages+1):
                # Montando a URL da página atual
                next_url = f"{url_pontos}/stop_times/?page={page_number}"
                response = await client.get(next_url)
                data = response.json()

                # Processar cada parada
                for item in data.get("results", []):
                    stop_info = item.get("stop_id", {})
                    route_info = item.get("trip_id", {}).get("route_id", {})

                    if stop_info and route_info:
                        parada = Pontos(
                            nome=stop_info.get("stop_name"),
                            lat=stop_info.get("stop_lat"),
                            lon=stop_info.get("stop_lon"),
                            sequencia=item.get("stop_sequence"),
                            linha=route_info.get("route_short_name"),
                            stop_id=stop_info.get("stop_id")  # Armazenando o stop_id mas não como chave primária
                        )

                        # Verificar se a combinação de 'stop_id' e 'linha' já existe
                        existing_parada = session.query(Pontos).filter(
                            Pontos.stop_id == parada.stop_id, 
                            Pontos.linha == parada.linha
                        ).first()

                        if not existing_parada:
                            # Se não existir, adiciona a nova parada
                            session.add(parada)
                        else:
                            # Se já existir, verifica se todos os campos são iguais
                            if (existing_parada.nome == parada.nome and
                                existing_parada.lat == parada.lat and
                                existing_parada.lon == parada.lon and
                                existing_parada.sequencia == parada.sequencia):
                                continue  # Não faz nada se os dados forem iguais
                            else:
                                # Atualiza os campos se houver alguma diferença
                                existing_parada.nome = parada.nome
                                existing_parada.lat = parada.lat
                                existing_parada.lon = parada.lon
                                existing_parada.sequencia = parada.sequencia

                # Commit da transação após processar a página inteira
                try:
                    session.commit()
                except IntegrityError as e:
                    print(f"Erro de integridade ao salvar dados da página {page_number}: {str(e)}")
                    session.rollback()

    except Exception as e:
        session.rollback()

    finally:
        session.close()