from pydantic import BaseModel
from datetime import datetime

class ConsultaBase(BaseModel):
    paciente_id: int
    profissional_id: int
    tipo: str
    status: str


class ConsultaCreate(ConsultaBase):
    pass


class ConsultaResponse(ConsultaBase):
    id: int
    data_hora: datetime

    class Config:
        from_attributes = True
