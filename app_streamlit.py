import streamlit as st
import requests
import base64
import json

API_URL = "http://localhost:8000"

# Estado de sesión
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None
if "usuario" not in st.session_state:
    st.session_state.usuario = {}
if "texto_revertido" not in st.session_state:
    st.session_state.texto_revertido = ""

st.set_page_config(page_title="Editor IA con LLaMA3", layout="centered")

# ----------------------
# FORMULARIO DE LOGIN
# ----------------------
if st.session_state.jwt_token is None:
    st.title("🔐 Iniciar sesión")
    with st.form("login"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submitted = st.form_submit_button("Iniciar sesión")

        if submitted:
            response = requests.post(f"{API_URL}/token", data={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                data = response.json()
                st.session_state.jwt_token = data["access_token"]

                # Decodificar JWT y guardar info de usuario
                token_parts = data["access_token"].split(".")
                payload = json.loads(base64.urlsafe_b64decode(token_parts[1] + "==").decode())
                st.session_state.usuario = payload
                st.success(f"Sesión iniciada como {payload['sub']} ({payload['role']})")
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas")
    st.stop()

# ----------------------
# CERRAR SESIÓN
# ----------------------
if st.button("🔓 Cerrar sesión"):
    st.session_state.jwt_token = None
    st.session_state.usuario = {}
    st.rerun()

# ----------------------
# CONTENIDO POR ROL
# ----------------------
rol = st.session_state.usuario.get("role")
headers = {"Authorization": f"Bearer {st.session_state.jwt_token}"}

# ----------------------
# REDACTOR
# ----------------------
if rol == "redactor":
    st.header("📝 Zona de redactor: Generación de texto con IA")

    texto = st.text_area("✍️ Escribe o pega tu texto aquí", value=st.session_state.texto_revertido)
    accion = st.selectbox("Acción a realizar", ["resumir", "corregir", "expandir", "variar"])

    if st.button("🚀 Mejorar texto"):
        res = requests.post(f"{API_URL}/mejorar", json={"texto": texto, "accion": accion}, headers=headers)
        if res.ok:
            resultado = res.json()["resultado"]
            version_id = res.json()["id_version"]
            st.text_area("📄 Resultado generado", value=resultado, height=300)
            st.code(f"ID de versión: {version_id}")
        else:
            st.error("❌ Error al generar texto")

# ----------------------
# APROBADOR
# ----------------------
elif rol == "aprobador":
    st.header("✅ Zona de aprobador: Revisión de contenido generado")

    res_hist = requests.get(f"{API_URL}/historial", headers=headers)
    if res_hist.ok:
        historial = res_hist.json()
        if historial:
            for item in reversed(historial[-5:]):
                with st.expander(f"{item['fecha']} — {item['accion']}"):
                    st.markdown("**📝 Texto generado:**")
                    st.text(item["resultado"])

                    # Mostrar comentarios
                    st.markdown("💬 Comentarios:")
                    res_com = requests.get(f"{API_URL}/version/{item['id']}/comentarios", headers=headers)
                    if res_com.ok and res_com.json():
                        for c in res_com.json():
                            st.markdown(f"**{c['autor']}** ({c['fecha']}): {c['contenido']}")
                    else:
                        st.info("Sin comentarios aún.")
        else:
            st.info("No hay contenido aún.")
    else:
        st.error("No se pudo cargar el historial.")

# ----------------------
# DISEÑADOR
# ----------------------
elif rol == "diseñador":
    st.header("🎨 Zona de diseñador (en construcción)")
    st.info("Aquí podrás revisar diseños generados por IA en el futuro.")

# ----------------------
# ROL NO VÁLIDO
# ----------------------
else:
    st.error("❌ Tu rol no tiene permisos válidos asignados.")

