from sqlalchemy.orm import Session
from app.DTO import usuarioDTO
from ..Repository import usuarioRepository


def criar_usuario(db: Session, usuario: usuarioDTO.UsuarioCreate):

    usuario_existente = db.query(usuarioRepository.Usuario).filter_by(login=usuario.login).first()
    if usuario_existente:
        raise ValueError("Login já está em uso.")
    
    email_existente = db.query(usuarioRepository.Usuario).filter_by(email=usuario.email).first()
    if email_existente:
        raise ValueError("Email já está em uso.")

    usuario_novo = usuarioRepository.Usuario(
        login=usuario.login,
        senha=usuario.senha,
        email=usuario.email
    )
    db.add(usuario_novo)
    db.commit()
    db.refresh(usuario_novo)
    return usuarioDTO.UsuarioOutInterno.model_validate(usuario_novo)


def autenticar_usuario(db: Session, login: str, senha: str):
    usuario = db.query(usuarioRepository.Usuario).filter_by(login=login).first()
    if not usuario or usuario.senha != senha:
        return None
    return usuarioDTO.UsuarioOutInterno.model_validate(usuario)



def listar_usuarios(db: Session):
    usuarios = db.query(usuarioRepository.Usuario).all()
    return [usuarioDTO.UsuarioBase.model_validate(u) for u in usuarios]


def atualizar_usuario(db: Session, usuario_id: int, dados: usuarioDTO.UsuarioUpdate):
    # Recupera o usuário a ser atualizado
    usuario = db.query(usuarioRepository.Usuario).filter(usuarioRepository.Usuario.id == usuario_id).first()
    
    if not usuario:
        return None

    # Verifica se o login já está em uso por outro usuário
    if dados.login and db.query(usuarioRepository.Usuario).filter(
        usuarioRepository.Usuario.login == dados.login, 
        usuarioRepository.Usuario.id != usuario_id  # Exclui o próprio usuário da verificação
    ).first():
        raise ValueError("Login já está em uso.")

    # Verifica se o e-mail já está em uso por outro usuário
    if dados.email and db.query(usuarioRepository.Usuario).filter(
        usuarioRepository.Usuario.email == dados.email,
        usuarioRepository.Usuario.id != usuario_id  # Exclui o próprio usuário da verificação
    ).first():
        raise ValueError("Email já está em uso.")

    # Atualiza os dados do usuário
    if dados.login:
        usuario.login = dados.login
    if dados.senha:
        usuario.senha = dados.senha
    if dados.email:
        usuario.email = dados.email

    db.commit()
    db.refresh(usuario)

    return usuarioDTO.UsuarioOutInterno.model_validate(usuario)



def obter_usuario_por_id(db: Session, usuario_id: int):
    # Busca o usuário diretamente com o ID
    usuario = db.query(usuarioRepository.Usuario).filter(usuarioRepository.Usuario.id == usuario_id).first()

    if not usuario:
        return None  

    return usuarioDTO.UsuarioOutInterno.model_validate(usuario)
