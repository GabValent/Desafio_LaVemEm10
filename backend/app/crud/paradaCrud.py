from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.Repository.paradaRepository import Parada
from app.DTO import paradaDTO

def criar_parada(db: Session, parada: paradaDTO.ParadaCreate) -> paradaDTO.ParadaOutInterno:
    nova_parada = Parada(
        usuario_id=parada.usuario_id,
        linha=parada.linha,
        ponto=parada.ponto,
        janela_horario_inicio=parada.janela_horario_inicio,
        janela_horario_fim=parada.janela_horario_fim,
        latitude=parada.latitude,
        longitude=parada.longitude
    )
    db.add(nova_parada)
    db.commit()
    db.refresh(nova_parada)
    return paradaDTO.ParadaOutInterno.model_validate(nova_parada)

def listar_parada(db: Session, parada_id: int) -> paradaDTO.ParadaBase | None:
    parada = db.query(Parada).filter(Parada.id == parada_id).first()
    if parada is None:
        return None
    return paradaDTO.ParadaBase.model_validate(parada)

def listar_paradas_por_usuario(db: Session, usuario_id: int) -> list[paradaDTO.ParadaOutInterno]:
    paradas = db.query(Parada).filter(Parada.usuario_id == usuario_id).all()
    return [paradaDTO.ParadaOutInterno.model_validate(p) for p in paradas]

def atualizar_parada(db: Session, parada_id: int, parada_data: paradaDTO.ParadaUpdate) -> paradaDTO.ParadaOutInterno | None:
    parada = db.query(Parada).filter(Parada.id == parada_id).first()
    if parada is None:
        return None

    if parada_data.linha is not None:
        parada.linha = parada_data.linha
    if parada_data.ponto is not None:
        parada.ponto = parada_data.ponto
    if parada_data.janela_horario_inicio is not None:    
        parada.janela_horario_inicio = parada_data.janela_horario_inicio
    if parada_data.janela_horario_fim is not None:    
        parada.janela_horario_fim = parada_data.janela_horario_fim
    if parada_data.latitude is not None:
        parada.latitude = parada_data.latitude
    if parada_data.longitude is not None:
        parada.longitude = parada_data.longitude

    db.commit()
    db.refresh(parada)
    return paradaDTO.ParadaOutInterno.model_validate(parada)

def deletar_parada(db: Session, parada_id: int) -> dict:
    parada = db.query(Parada).filter(Parada.id == parada_id).first()

    if not parada:
        raise HTTPException(status_code=404, detail="Parada não encontrada")

    db.delete(parada)
    db.commit()
    return {"detail": f"Parada {parada_id} deletada com sucesso"}
