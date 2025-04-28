from datetime import timedelta
from celery import Celery


# Configuração do Celery com o Redis
celery = Celery("tasks", broker="redis://redis:6379/0", include=["app.tasks"])


# Carregar as configurações do arquivo de configuração
celery.conf.beat_schedule = {
    'consultar_dados_onibus': {
        'task': 'app.tasks.consultar_dados_onibus', 
        'schedule': 60.0, 
    },
    'enviar_emails': {
        'task': 'app.tasks.enviar_emails',
        'schedule': 61.0,
    },
    'atualizar_linhas_onibus' :{
        "task": "app.tasks.atualizar_linhas_onibus",
        "schedule":86400,
    }
}

celery.conf.timezone = "UTC"

import app.tasks
