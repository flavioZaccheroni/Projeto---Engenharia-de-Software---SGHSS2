from fastapi import FastAPI
from app.database import Base, engine

from app.models import consulta
from app.models.paciente import Paciente
from app.models.usuario import Usuario
from app.models.profissional import ProfissionalSaude
from app.models.consulta import Consulta
from app.models.prontuario import Prontuario

from app.routes import pacientes, profissionais, consultas, auth, prontuario

app = FastAPI(title="SGHSS - Back-end")

Base.metadata.create_all(bind=engine)

app.include_router(pacientes.router)
app.include_router(profissionais.router)
app.include_router(consultas.router)
app.include_router(auth.router)
app.include_router(prontuario.router)

@app.get("/")
def root():
    return {"status": "SGHSS API funcionando corretamente"}

