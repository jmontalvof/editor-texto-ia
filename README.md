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

