from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db import Usuario, SessionLocal

SECRET_KEY = "secreto-super-seguro"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def obtener_sesion():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def autenticar_usuario(db: Session, username: str, password: str):
    user = db.query(Usuario).filter(Usuario.username == username).first()
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

def crear_token(usuario: Usuario):
    data = {"sub": usuario.username, "role": usuario.role}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

def requerir_rol(rol_requerido: str):
    def validador(usuario=Depends(obtener_usuario_actual)):
        if usuario["role"] != rol_requerido:
            raise HTTPException(status_code=403, detail="Permiso denegado")
        return usuario
    return validador

