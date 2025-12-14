from app.security.auth import obter_usuario_logado
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.paciente import Paciente
from app.schemas.paciente_schema import PacienteCreate, PacienteResponse

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

# Dependência do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# CREATE - Criar paciente
@router.post("/", response_model=PacienteResponse)
def criar_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    paciente_existente = db.query(Paciente).filter(Paciente.cpf == paciente.cpf).first()
    if paciente_existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    novo_paciente = Paciente(**paciente.dict())
    db.add(novo_paciente)
    db.commit()
    db.refresh(novo_paciente)
    return novo_paciente


# READ - Listar todos os pacientes
@router.get("/", response_model=list[PacienteResponse])
def listar_pacientes(
    usuario=Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    return db.query(Paciente).all()



# READ - Buscar paciente por ID
@router.get("/{paciente_id}", response_model=PacienteResponse)
def buscar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente


# DELETE - Remover paciente
@router.delete("/{paciente_id}")
def remover_paciente(
    paciente_id: int,
    usuario=Depends(obter_usuario_logado),
    db: Session = Depends(get_db)
):
    if usuario["perfil"] != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Acesso permitido apenas para administradores"
        )

    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    db.delete(paciente)
    db.commit()
    return {"message": "Paciente removido com sucesso"}

