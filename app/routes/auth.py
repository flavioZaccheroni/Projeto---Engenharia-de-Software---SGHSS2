from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.usuario import Usuario
from app.security.hash import verificar_senha
from app.security.auth import criar_token

router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()

    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token({
        "sub": usuario.email,
        "perfil": usuario.perfil
    })

    return {"access_token": token, "token_type": "bearer"}
