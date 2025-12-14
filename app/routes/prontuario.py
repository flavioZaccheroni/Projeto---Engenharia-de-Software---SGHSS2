from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.prontuario import Prontuario
from app.models.consulta import Consulta
from app.schemas.prontuario_schema import (
    ProntuarioCreate,
    ProntuarioResponse
)
from app.security.auth import obter_usuario_logado

router = APIRouter(
    prefix="/prontuarios",
    tags=["Prontuários"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE - Criar prontuário (somente PROFISSIONAL)
@router.post("/", response_model=ProntuarioResponse)
def criar_prontuario(
    prontuario: ProntuarioCreate,
    usuario=Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    if usuario["perfil"] != "PROFISSIONAL":
        raise HTTPException(
            status_code=403,
            detail="Somente profissionais de saúde podem registrar prontuários"
        )

    consulta = db.query(Consulta).filter(
        Consulta.id == prontuario.consulta_id
    ).first()

    if not consulta:
        raise HTTPException(
            status_code=404,
            detail="Consulta não encontrada"
        )

    novo = Prontuario(**prontuario.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# READ - Listar prontuários
@router.get("/", response_model=list[ProntuarioResponse])
def listar_prontuarios(
    usuario=Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    return db.query(Prontuario).all()


# READ - Buscar prontuário por ID
@router.get("/{prontuario_id}", response_model=ProntuarioResponse)
def buscar_prontuario(
    prontuario_id: int,
    usuario=Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    prontuario = db.query(Prontuario).filter(
        Prontuario.id == prontuario_id
    ).first()

    if not prontuario:
        raise HTTPException(
            status_code=404,
            detail="Prontuário não encontrado"
        )

    return prontuario
