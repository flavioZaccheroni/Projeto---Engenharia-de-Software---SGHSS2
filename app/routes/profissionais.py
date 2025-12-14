from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.profissional import ProfissionalSaude
from app.schemas.profissional_schema import (
    ProfissionalCreate,
    ProfissionalResponse
)

router = APIRouter(
    prefix="/profissionais",
    tags=["Profissionais de Saúde"]
)

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE - Criar profissional
@router.post("/", response_model=ProfissionalResponse)
def criar_profissional(
    profissional: ProfissionalCreate,
    db: Session = Depends(get_db)
):
    existente = db.query(ProfissionalSaude).filter(
        ProfissionalSaude.crm == profissional.crm
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="CRM já cadastrado"
        )

    novo = ProfissionalSaude(**profissional.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# READ - Listar profissionais
@router.get("/", response_model=list[ProfissionalResponse])
def listar_profissionais(db: Session = Depends(get_db)):
    return db.query(ProfissionalSaude).all()


# READ - Buscar por ID
@router.get("/{profissional_id}", response_model=ProfissionalResponse)
def buscar_profissional(
    profissional_id: int,
    db: Session = Depends(get_db)
):
    profissional = db.query(ProfissionalSaude).filter(
        ProfissionalSaude.id == profissional_id
    ).first()

    if not profissional:
        raise HTTPException(
            status_code=404,
            detail="Profissional não encontrado"
        )

    return profissional


# DELETE - Remover profissional
@router.delete("/{profissional_id}")
def remover_profissional(
    profissional_id: int,
    db: Session = Depends(get_db)
):
    profissional = db.query(ProfissionalSaude).filter(
        ProfissionalSaude.id == profissional_id
    ).first()

    if not profissional:
        raise HTTPException(
            status_code=404,
            detail="Profissional não encontrado"
        )

    db.delete(profissional)
    db.commit()
    return {"message": "Profissional removido com sucesso"}
