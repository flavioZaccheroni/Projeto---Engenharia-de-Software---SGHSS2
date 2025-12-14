from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    telefone = Column(String(20))