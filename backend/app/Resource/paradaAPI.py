from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.DTO import paradaDTO
from app.crud import paradaCrud
from app.database import get_db

router = APIRouter()

@router.post("/criar", response_model=paradaDTO.ParadaOutInterno)
def criar_parada(parada: paradaDTO.ParadaCreate, db: Session = Depends(get_db)):
    return paradaCrud.criar_parada(db, parada)

@router.get("/usuario/{usuario_id}", response_model=list[paradaDTO.ParadaOutInterno])
def listar_paradas_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return paradaCrud.listar_paradas_por_usuario(db, usuario_id)

@router.put("/{parada_id}", response_model=paradaDTO.ParadaOutInterno)
def editar_parada(parada_id: int, parada_data: paradaDTO.ParadaUpdate, db: Session = Depends(get_db)):
    parada = paradaCrud.atualizar_parada(db, parada_id, parada_data)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    return parada

@router.delete("/{parada_id}")
def deletar_parada(parada_id: int, db: Session = Depends(get_db)):
    parada = paradaCrud.deletar_parada(db, parada_id)
    if not parada:
        raise HTTPException(status_code=404, detail="Parada não encontrada")
    return {"detail": "Parada deletada com sucesso"}
