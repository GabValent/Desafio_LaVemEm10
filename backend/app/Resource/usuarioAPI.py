from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import usuarioCrud
from app.database import get_db
from app.DTO import usuarioDTO

router = APIRouter()

@router.post("/criar", response_model=usuarioDTO.UsuarioOutInterno)
def criar_usuario(usuario: usuarioDTO.UsuarioCreate, db: Session = Depends(get_db)):
    print(" Criando usuário:", usuario.login)
    try:
        return usuarioCrud.criar_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=usuarioDTO.UsuarioOutInterno)
def login(dados: usuarioDTO.UsuarioLogin, db: Session = Depends(get_db)):
    usuario = usuarioCrud.autenticar_usuario(db, dados.login, dados.senha)
    if not usuario:
        raise HTTPException(status_code=401, detail="Login ou senha incorretos")
    return usuario


@router.get("/list", response_model=list[usuarioDTO.UsuarioBase])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuarioCrud.listar_usuarios(db)

@router.put("/{usuario_id}", response_model=usuarioDTO.UsuarioOutInterno)
def editar_usuario(usuario_id: int, dados: usuarioDTO.UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = usuarioCrud.atualizar_usuario(db, usuario_id, dados)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.get("/{usuario_id}", response_model=usuarioDTO.UsuarioOutInterno)
def obter_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuarioCrud.obter_usuario_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario
