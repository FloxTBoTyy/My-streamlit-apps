import streamlit as st
import pandas as pd

# Inicializar datos en sesión
if 'pacientes' not in st.session_state:
    st.session_state.pacientes = []

st.title("📋 Registro de Signos Vitales - Enfermería")
st.markdown("Aplicación simple para registrar pacientes y ver sus signos vitales.")

# Formulario de registro
with st.form("registro_paciente"):
    st.subheader("📝 Registrar nuevo paciente")

    nombre = st.text_input("Nombre del paciente")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=45.0, step=0.1)
    presion_sistolica = st.number_input("Presión sistólica (mmHg)", min_value=50, max_value=200)
    presion_diastolica = st.number_input("Presión diastólica (mmHg)", min_value=30, max_value=150)
    frecuencia = st.number_input("Frecuencia cardíaca (lpm)", min_value=30, max_value=180)

    submitted = st.form_submit_button("Registrar")

    if submitted:
        st.session_state.pacientes.append({
            "Nombre": nombre,
            "Edad": edad,
            "Temperatura (°C)": temperatura,
            "Presión arterial": f"{presion_sistolica}/{presion_diastolica}",
            "Frecuencia cardíaca (lpm)": frecuencia
        })
        st.success(f"✅ Paciente '{nombre}' registrado con éxito.")

# Mostrar pacientes
st.subheader("📊 Pacientes Registrados")
if st.session_state.pacientes:
    df = pd.DataFrame(st.session_state.pacientes)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aún no hay pacientes registrados.")

