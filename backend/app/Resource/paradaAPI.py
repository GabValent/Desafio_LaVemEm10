import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.DTO import paradaDTO
from app.crud import paradaCrud
from app.database import get_db

# Configura o logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/criar", response_model=paradaDTO.ParadaOutInterno, status_code=status.HTTP_201_CREATED)
def criar_parada(parada: paradaDTO.ParadaCreate, db: Session = Depends(get_db)):
    logger.info(f"Criando parada para linha {parada.linha}")
    return paradaCrud.criar_parada(db, parada)

@router.get("/usuario/{usuario_id}", response_model=list[paradaDTO.ParadaOutInterno])
def listar_paradas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    logger.info(f"Listando paradas do usuário ID {usuario_id}")
    return paradaCrud.listar_paradas_por_usuario(db, usuario_id)

@router.put("/{parada_id}", response_model=paradaDTO.ParadaOutInterno)
def editar_parada(parada_id: int, parada_data: paradaDTO.ParadaUpdate, db: Session = Depends(get_db)):
    logger.info(f"Editando parada ID {parada_id}")
    parada = paradaCrud.atualizar_parada(db, parada_id, parada_data)
    if not parada:
        logger.warning(f"Parada ID {parada_id} não encontrada.")
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    return parada

@router.delete("/{parada_id}")
def deletar_parada(parada_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deletando parada ID {parada_id}")
    parada = paradaCrud.deletar_parada(db, parada_id)
    if not parada:
        logger.warning(f"Parada ID {parada_id} não encontrada.")
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    return {"detail": "Parada deletada com sucesso"}
