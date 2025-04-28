import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import usuarioCrud
from app.database import get_db
from app.DTO import usuarioDTO

# Configura o logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

@router.post("/criar", response_model=usuarioDTO.UsuarioOutInterno, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario: usuarioDTO.UsuarioCreate, db: Session = Depends(get_db)):
    logger.info(f"Criando usuário: {usuario.login}")
    try:
        return usuarioCrud.criar_usuario(db, usuario)
    except ValueError as e:
        logger.error(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    

@router.post("/login", response_model=usuarioDTO.UsuarioOutInterno)
def login(dados: usuarioDTO.UsuarioLogin, db: Session = Depends(get_db)):
    logger.info(f"Login tentativa: {dados.login}")
    usuario = usuarioCrud.autenticar_usuario(db, dados.login, dados.senha)
    if not usuario:
        logger.warning(f"Falha de login para usuário: {dados.login}")
        raise HTTPException(status_code=401, detail="Login ou senha incorretos")
    return usuario


@router.get("/list", response_model=list[usuarioDTO.UsuarioBase])
def listar_usuarios(db: Session = Depends(get_db)):
    logger.info("Listando usuários.")
    return usuarioCrud.listar_usuarios(db)

@router.put("/{usuario_id}", response_model=usuarioDTO.UsuarioOutInterno)
def editar_usuario(usuario_id: int, dados: usuarioDTO.UsuarioUpdate, db: Session = Depends(get_db)):
    logger.info(f"Editando usuário ID: {usuario_id}")
    usuario = usuarioCrud.atualizar_usuario(db, usuario_id, dados)
    if usuario is None:
        logger.warning(f"Usuário ID {usuario_id} não encontrado para edição.")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@router.get("/{usuario_id}", response_model=usuarioDTO.UsuarioOutInterno)
def obter_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    logger.info(f"Buscando usuário ID: {usuario_id}")
    usuario = usuarioCrud.obter_usuario_por_id(db, usuario_id)
    if not usuario:
        logger.warning(f"Usuário ID {usuario_id} não encontrado.")
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuario
