# ✨ Editor de Texto con IA (LLaMA3 + FastAPI + Streamlit)

Aplicación web inteligente que permite generar, corregir, resumir y expandir texto con modelos locales como **LLaMA3**, usando **Ollama** en tu máquina y una interfaz web creada con **Streamlit** y **FastAPI**.
Cuenta con autenticación, control por roles y funcionalidad colaborativa mediante comentarios por versión.

---

## 🚀 Funcionalidades principales

✅ Login seguro con JWT
✅ Roles con permisos personalizados (`redactor`, `aprobador`, `diseñador`)
✅ Generación de texto vía IA (LLaMA3 + Ollama)
✅ Historial de versiones
✅ Reversión de contenido
✅ Comentarios colaborativos por versión
✅ Frontend interactivo con Streamlit
✅ Backend robusto con FastAPI + SQLite

---

## 🧱 Estructura del proyecto

```text
editor-texto-ia/
├── app_streamlit.py         # Interfaz web por rol
├── main.py                  # API FastAPI
├── auth.py                  # Login y control de roles
├── db.py                    # Modelos SQLAlchemy + conexión
├── historial.py             # Manejo de versiones
├── llama3_local.py          # Conexión a Ollama
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Imagen Docker de la app
├── docker-compose.yml       # Orquestador de contenedores
└── .dockerignore
```

---

## ⚙️ Requisitos previos

* Tener [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados
* Tener [Ollama](https://ollama.com/) instalado y funcionando localmente

Ejecuta Ollama en tu máquina antes de lanzar la app:

```bash
ollama run llama3
```

---

## 🐳 Cómo ejecutar con Docker

1. Clona el repositorio:

```bash
git clone https://github.com/jmontalvof/editor-texto-ia.git
cd editor-texto-ia
```

2. Ejecuta el proyecto:

```bash
docker-compose up --build
```

3. Accede a la aplicación:

* 📁 API (FastAPI): [http://localhost:8000/docs](http://localhost:8000/docs)
* 💻 Interfaz web (Streamlit): [http://localhost:8501](http://localhost:8501)

---

## 🔐 Crear usuarios

Visita `http://localhost:8000/docs` y usa el endpoint:

```
POST /registro
```

Ejemplo:

```json
{
  "username": "jorge",
  "password": "1234",
  "role": "redactor"
}
```

---

## 👥 Roles disponibles

| Rol         | Permisos disponibles                        |
| ----------- | ------------------------------------------- |
| `redactor`  | Generar texto, ver historial personal       |
| `aprobador` | Ver historial completo, revisar comentarios |
| `diseñador` | (Reservado para funciones visuales futuras) |

---

## 📝 Dependencias clave

* `fastapi`
* `uvicorn`
* `sqlalchemy`
* `streamlit`
* `requests`
* `python-jose[cryptography]`
* `passlib[bcrypt]`
* `python-multipart`

---

## ⚙️ Personalización

Si usas Docker y Ollama está instalado fuera del contenedor, asegúrate de que en `llama3_local.py` se use:

```python
OLLAMA_URL = "http://host.docker.internal:11434"
```

Esto permite que Docker se conecte a Ollama en tu máquina.

---

## 🤝 Contribuciones

Pull requests bienvenidas. Puedes colaborar en nuevas funcionalidades como:

* Comparación visual entre versiones
* Integración con otros modelos
* Dashboard de estadísticas

---

## 👤 Autor

Proyecto creado por **Jorge**, combinando FastAPI, Streamlit y modelos locales con Ollama para construir una plataforma colaborativa de edición de texto con IA.

---

## 🔒 Ética y seguridad en IA generativa

Esta aplicación está diseñada siguiendo principios éticos y medidas de seguridad que refuerzan su uso responsable:

### 🔏 Privacidad y cifrado

* Contenido y versiones pueden cifrarse antes de ser almacenados.
* Se recomienda el uso de HTTPS con certificados SSL.
* JWT firmados y con expiración para autenticación segura.

### 🏛️ Uso ético y derechos de autor

* Políticas claras de uso mostradas en la interfaz (Streamlit).
* Prohibición de prompts con violencia, odio o lenguaje discriminatorio.
* Advertencia legal sobre el uso de contenido generado por IA.

### 🕵️️ Moderación y control de contenido

* El rol `aprobador` puede revisar versiones antes de validarlas.
* Se pueden integrar filtros automáticos de contenido sensible (profanidad, hate speech).
* Cada versión podrá tener un estado: `pendiente`, `aprobado`, `rechazado`.

Estas medidas permiten que la IA generativa sea utilizada de forma segura, respetuosa y legal.

