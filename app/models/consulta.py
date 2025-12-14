from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, nullable=False)
    profissional_id = Column(Integer, nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)
    tipo = Column(String(20))  # PRESENCIAL ou TELEMEDICINA
    status = Column(String(20))  # AGENDADA, CANCELADA, FINALIZADA
