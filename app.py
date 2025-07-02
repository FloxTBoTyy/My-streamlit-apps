import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
#from data import openings_df, hardware_df

st.set_page_config(layout="wide")
st.title("🛠️ Install Planning + Field Checklist")

openings_df = pd.read_csv("openings.csv")
hardware_df = pd.read_csv("hardware.csv")
# Filtros
with st.sidebar:
    st.header("Filtros")
    project = st.selectbox("Proyecto", openings_df["Project"].unique())
    area = st.selectbox("Área", openings_df[openings_df["Project"] == project]["Area"].unique())
    floor = st.selectbox("Piso", openings_df[
        (openings_df["Project"] == project) & 
        (openings_df["Area"] == area)
    ]["Floor"].unique())

    filtered_openings = openings_df[
        (openings_df["Project"] == project) &
        (openings_df["Area"] == area) &
        (openings_df["Floor"] == floor)
    ]

opening_selected = st.selectbox("Selecciona una apertura", filtered_openings["Opening ID"])

# Datos de la apertura seleccionada
opening_row = filtered_openings[filtered_openings["Opening ID"] == opening_selected].iloc[0]
hw_group = opening_row["Hardware Group"]

components = hardware_df[hardware_df["Hardware Group"] == hw_group].copy()
components["Opening"] = opening_selected
components["Door Type"] = opening_row["Door Type"]
components["Frame Type"] = opening_row["Frame Type"]
components["Hdw Set"] = hw_group
components["Time - Frame"] = ""
components["Time - Door"] = ""
components["Time - Hardware"] = ""

# Reorganizar columnas
components = components[[
    "Opening", "Door Type", "Frame Type", "Hdw Set",
    "Component", "Description", "Finish", "Notes",
    "Time - Frame", "Time - Door", "Time - Hardware"
]]

st.subheader(f"Checklist para: {opening_selected}")
st.dataframe(components, use_container_width=True)

# QR opcional
# Tu nombre de app en Streamlit
APP_URL = "https://planning-checklist.streamlit.app"
# QR dinámico por apertura
qr_url = f"{APP_URL}/?opening={opening_selected}"
qr = qrcode.make(qr_url)
buf = BytesIO()
qr.save(buf)
st.image(buf.getvalue(), caption=f"QR: {qr_url}", width=150)

# Exportar a Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name="Checklist")
    return output.getvalue()

st.download_button(
    label="📥 Exportar checklist a Excel",
    data=to_excel(components),
    file_name=f"checklist_{opening_selected}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
