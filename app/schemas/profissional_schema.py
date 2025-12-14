from pydantic import BaseModel

class ProfissionalBase(BaseModel):
    nome: str
    crm: str
    especialidade: str | None = None


class ProfissionalCreate(ProfissionalBase):
    pass


class ProfissionalResponse(ProfissionalBase):
    id: int

    class Config:
        from_attributes = True
