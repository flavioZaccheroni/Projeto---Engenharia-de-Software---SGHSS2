from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Prontuario(Base):
    __tablename__ = "prontuarios"

    id = Column(Integer, primary_key=True, index=True)
    consulta_id = Column(Integer, nullable=False)
    descricao = Column(String)
    prescricao = Column(String)
    data_registro = Column(DateTime, default=datetime.utcnow)
