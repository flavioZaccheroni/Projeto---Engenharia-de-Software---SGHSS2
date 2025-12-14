from pydantic import BaseModel

class PacienteBase(BaseModel):
    nome: str
    cpf: str
    telefone: str | None = None


class PacienteCreate(PacienteBase):
    pass


class PacienteResponse(PacienteBase):
    id: int

    class Config:
        from_attributes = True

