from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./usuarios.db"
Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class Usuario(Base):
    __tablename__ = "usuarios"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # redactor, diseñador, aprobador

def crear_bd():
    Base.metadata.create_all(bind=engine)

from sqlalchemy import ForeignKey, DateTime, Text
from datetime import datetime

class Comentario(Base):
    __tablename__ = "comentarios"
    id = Column(String, primary_key=True, index=True)
    version_id = Column(String, index=True)
    autor = Column(String, ForeignKey("usuarios.username"))
    contenido = Column(Text)
    fecha = Column(DateTime, default=datetime.utcnow)

