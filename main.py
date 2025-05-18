from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import crear_bd, SessionLocal, Usuario, Comentario
from auth import (
    obtener_sesion, autenticar_usuario, crear_token,
    obtener_usuario_actual, requerir_rol
)
from historial import guardar_version, obtener_historial, obtener_version_por_id
from llama3_local import mejorar_texto_llama3
from uuid import uuid4

app = FastAPI()
crear_bd()

# ----------------------
# REGISTRO DE USUARIO
# ----------------------
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/registro")
def registrar(username: str, password: str, role: str, db=Depends(obtener_sesion)):
    if db.query(Usuario).filter(Usuario.username == username).first():
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    nuevo = Usuario(
        username=username,
        hashed_password=pwd_context.hash(password),
        role=role
    )
    db.add(nuevo)
    db.commit()
    return {"mensaje": "Usuario creado correctamente"}

# ----------------------
# LOGIN JWT
# ----------------------
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(obtener_sesion)):
    user = autenticar_usuario(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Credenciales inválidas")
    token = crear_token(user)
    return {"access_token": token, "token_type": "bearer"}

# ----------------------
# PROTECCIÓN POR ROL
# ----------------------
@app.get("/solo-redactor")
def ruta_redactor(usuario=Depends(requerir_rol("redactor"))):
    return {"mensaje": f"Bienvenido redactor {usuario['sub']}"}

# ----------------------
# MEJORAR TEXTO
# ----------------------
class Peticion(BaseModel):
    texto: str
    accion: str  # 'resumir', 'corregir', 'expandir', 'variar'

@app.post("/mejorar")
def mejorar_texto(peticion: Peticion, usuario=Depends(obtener_usuario_actual)):
    resultado = mejorar_texto_llama3(peticion.texto, peticion.accion)
    version_id = guardar_version(peticion.texto, peticion.accion, resultado)
    return {"resultado": resultado, "id_version": version_id}

# ----------------------
# HISTORIAL
# ----------------------
@app.get("/historial")
def ver_historial():
    return obtener_historial()

@app.get("/version/{version_id}")
def ver_version(version_id: str):
    version = obtener_version_por_id(version_id)
    if version:
        return version
    return {"error": "Versión no encontrada"}

# ----------------------
# COMENTARIOS
# ----------------------
class ComentarioInput(BaseModel):
    version_id: str
    contenido: str

@app.post("/version/{version_id}/comentario")
def agregar_comentario(version_id: str, comentario: ComentarioInput, usuario=Depends(obtener_usuario_actual), db: Session = Depends(obtener_sesion)):
    nuevo = Comentario(
        id=str(uuid4()),
        version_id=version_id,
        autor=usuario["sub"],
        contenido=comentario.contenido
    )
    db.add(nuevo)
    db.commit()
    return {"mensaje": "Comentario agregado"}

@app.get("/version/{version_id}/comentarios")
def listar_comentarios(version_id: str, db: Session = Depends(obtener_sesion)):
    resultados = db.query(Comentario).filter(Comentario.version_id == version_id).all()
    return [{"autor": c.autor, "contenido": c.contenido, "fecha": c.fecha.isoformat()} for c in resultados]

