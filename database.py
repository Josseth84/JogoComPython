from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Substitua com suas credenciais reais
DATABASE_URL = "postgresql://jose_user:NEWlocal001!@localhost:5432/jogocompython"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)