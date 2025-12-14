from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.consulta import Consulta
from app.models.paciente import Paciente
from app.models.profissional import ProfissionalSaude
from app.schemas.consulta_schema import ConsultaCreate, ConsultaResponse

router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)

# Dependência do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE - Criar consulta
@router.post("/", response_model=ConsultaResponse)
def criar_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):

    paciente = db.query(Paciente).filter(
        Paciente.id == consulta.paciente_id
    ).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    profissional = db.query(ProfissionalSaude).filter(
        ProfissionalSaude.id == consulta.profissional_id
    ).first()
    if not profissional:
        raise HTTPException(status_code=404, detail="Profissional não encontrado")

    nova_consulta = Consulta(**consulta.dict())
    db.add(nova_consulta)
    db.commit()
    db.refresh(nova_consulta)
    return nova_consulta


# READ - Listar consultas
@router.get("/", response_model=list[ConsultaResponse])
def listar_consultas(db: Session = Depends(get_db)):
    return db.query(Consulta).all()


# READ - Buscar por ID
@router.get("/{consulta_id}", response_model=ConsultaResponse)
def buscar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")
    return consulta


# DELETE - Cancelar consulta
@router.delete("/{consulta_id}")
def cancelar_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta não encontrada")

    db.delete(consulta)
    db.commit()
    return {"message": "Consulta cancelada com sucesso"}
