from pydantic import BaseModel
from datetime import datetime

class ProntuarioBase(BaseModel):
    consulta_id: int
    descricao: str
    prescricao: str


class ProntuarioCreate(ProntuarioBase):
    pass


class ProntuarioResponse(ProntuarioBase):
    id: int
    data_registro: datetime

    class Config:
        from_attributes = True
