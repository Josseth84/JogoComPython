from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Resposta(Base):
    __tablename__ = "resposta"

    id = Column(Integer, primary_key=True, index=True)
    jogador = Column(String(100), nullable=False)
    fase = Column(Integer, nullable=False)
    escolha = Column(String(200), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tempo_resposta = Column(Float, nullable=True)  # Tempo em segundos