from datetime import datetime, timedelta
from sqlite3 import IntegrityError
from app.database import SessionLocal
from app.Repository.paradaRepository import Parada
from app.Repository.emailRepository import EmailRegistro
from app.Repository.usuarioRepository import Usuario
from app.Repository.onibusRepository import Onibus
from app.Repository.pontosRepository import Pontos
from app.celery_worker import celery
from app.Services.enviarEmail import enviar_email
from zoneinfo import ZoneInfo
from app.Services.filtrarLinha import filtrar_onibus_por_linha
from app.Services.calcularDistancia import calcularDistancia
import requests
import httpx
import redis
import json

url_base = "https://dados.mobilidade.rio/gps/sppo"
url_onibus = "https://api.mobilidade.rio/gtfs/routes/"
travel_time_url = "https://api.traveltimeapp.com/v4/time-filter"
url_pontos = "https://api.mobilidade.rio/gtfs"
redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)


@celery.task
def consultar_dados_onibus():
    tempo_agora = datetime.now(ZoneInfo("America/Sao_Paulo"))
    tempo_agoraMenosUm = tempo_agora - timedelta(minutes=1)

    # Request de um minuto atrás
    data_inicial = tempo_agoraMenosUm.strftime("%Y-%m-%d %H:%M:%S")
    data_final = tempo_agora.strftime("%Y-%m-%d %H:%M:%S")

    url_completa = f"{url_base}?dataInicial={data_inicial}&dataFinal={data_final}"

    db = SessionLocal()

    try:
        response = requests.get(url_completa, timeout=20)

        if response.status_code == 200:
            response_json = response.json()


            paradas = db.query(Parada).all()
            dez_minutos_atras = datetime.now(ZoneInfo("America/Sao_Paulo")) - timedelta(minutes=10)

            for parada in paradas:
                json_linha = filtrar_onibus_por_linha(response_json, parada.linha)

              

                distancia = calcularDistancia(json_linha, parada.id)


                redis_key = f"linha:{parada.linha}"
                redis_client.set(redis_key, json.dumps(distancia), ex=60)

                envia_email = False
                horario_fim_segundos = parada.janela_horario_fim.hour * 3600 + parada.janela_horario_fim.minute * 60 + parada.janela_horario_fim.second
                horario_inicio_segundos = parada.janela_horario_inicio.hour * 3600 + parada.janela_horario_inicio.minute * 60 + parada.janela_horario_inicio.second
                diferenca_tempo = horario_fim_segundos - horario_inicio_segundos


                horario_atual_segundos = tempo_agora.hour * 3600 + tempo_agora.minute * 60 + tempo_agora.second
                if horario_inicio_segundos <= horario_atual_segundos <= horario_fim_segundos:
                    for onibus in distancia:
                        if onibus["tempo_chegada"] < 600 + diferenca_tempo:
                            envia_email = True

                if envia_email:
                    # Verifica se já existe um e-mail registrado nos últimos 10 minutos
                    email_existente = db.query(EmailRegistro).filter(
                        EmailRegistro.linha == parada.linha,
                        EmailRegistro.usuario_id == parada.usuario_id,
                        EmailRegistro.horario >= dez_minutos_atras
                    ).first()

                    if not email_existente:
                        # Criação de um novo registro de e-mail
                        email_registro = EmailRegistro(
                            usuario_id=parada.usuario_id,
                            linha=parada.linha,
                            horario=datetime.now(ZoneInfo("America/Sao_Paulo")),
                            enviado=False
                        )
                        db.add(email_registro)
                        db.commit()
        else:
            print(f"Erro ao consultar API externa. Status: {response.status_code}")

    except Exception as e:
        print(f"Erro geral ao consultar a API: {e}")

    finally:
        db.close()


@celery.task
def enviar_emails():
    db = SessionLocal()
    pendentes = db.query(EmailRegistro).filter(EmailRegistro.enviado == False).all()

    for registro in pendentes:
        usuario = db.query(Usuario).filter(Usuario.id == registro.usuario_id).first()

        if usuario:
            try:
                conteudo = f"""
                <p>Olá,</p>
                <p>O ônibus da <strong>linha {registro.linha}</strong> deve chegar em menos de 10 minutos ao ponto que você cadastrou.</p>
                <p>Tenha um bom dia!</p>
                """
                enviar_email(usuario.email, "Seu ônibus está próximo!", conteudo)
                registro.enviado = True
                db.commit()
            except Exception as e:
                print(f" Falha ao enviar e-mail para {usuario.email}: {e}")

    db.close()



@celery.task
def atualizar_linhas_onibus():
    db = SessionLocal()
    try:
        db.query(Onibus).delete()
        db.commit()

        url = url_onibus
        with httpx.Client(timeout=30.0) as client:
            while url:
                response = client.get(url)
                if response.status_code != 200:
                    break

                data = response.json()

                for item in data.get("results", []):
                    numero = item.get("route_short_name")
                    nome = item.get("route_long_name")
                    branding = item.get("route_branding_url")

                    # Verificar se o branding é "BRT", e ignorar esses itens
                    if branding == "BRT":
                        continue

                    if numero and nome:
                        novo = Onibus(numero_linha=numero, nome_linha=nome)
                        db.add(novo)

                db.commit()
                url = data.get("next")

        print("Resposta JSON:", response)

    except Exception as e:
        print(f"Erro ao atualizar linhas de ônibus: {e}")
    finally:
        db.close()





