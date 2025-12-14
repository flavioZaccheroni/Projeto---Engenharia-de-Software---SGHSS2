from sqlalchemy import Column, Integer, String
from app.database import Base

class ProfissionalSaude(Base):
    __tablename__ = "profissionais_saude"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(String(100))
