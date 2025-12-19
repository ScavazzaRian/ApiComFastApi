import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Carregando as variaveis do .env
load_dotenv()

# Recuperando as variaveis de acesso da env
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PW")
db = os.getenv("POSTGRES_DB")

# Montando a conexao com o db
SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@localhost:5432/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()