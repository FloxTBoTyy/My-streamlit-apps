import streamlit as st
import pandas as pd
import numpy as np
import math
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

# Estilo básico con markdown
st.markdown(
    """
    <style>
    .big-font {
        font-size:40px !important;
        font-weight: 700;
        color: #0A74DA;
        text-align: center;
    }
    .subtitle {
        font-size:20px !important;
        font-weight: 500;
        color: #555;
        margin-bottom: 10px;
    }
    .section-header {
        font-size:18px !important;
        font-weight: 600;
        color: #0A74DA;
        margin-top: 20px;
        margin-bottom: 5px;
    }
    .footer-text {
        font-size:12px !important;
        color: #888;
        margin-top: 50px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="big-font">PDF Report Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Please upload your excel file</p>', unsafe_allow_html=True)
st.markdown("---")

uploaded_file = st.file_uploader("📁 Upload your excel file here (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    with st.spinner('Processing your file and generating your PDF... 🚀'):
        # Leer datos
        BOQ_ALL = pd.read_excel(uploaded_file, sheet_name="BOQ ALL", header=None)
        door_schedule = pd.read_excel(uploaded_file, sheet_name="Door Schedule")
        hardware = pd.read_excel(uploaded_file, sheet_name="Hardware")

        project = BOQ_ALL.iloc[0, 2]
        location = BOQ_ALL.iloc[1, 2]
        columns_hardware = ["Set Qty", "Hardware Description ", "Catalog Number", "Installed", "Verified", "Est hours"]

        openings_list = door_schedule.Opening.to_list()
        building_area_list = door_schedule["Building Area"].to_list()
        hardware_set_list = door_schedule["HDW Set"].to_list()
        hardware_set_list = [int(x) if isinstance(x, float) and not math.isnan(x) else x for x in hardware_set_list]
        hardware_set_list_str = [f"{int(x):02}" if str(x).isdigit() and (not math.isnan(x))
                                else x if isinstance(x,str)
                                else "NA"
                                for x in hardware_set_list]
        fire_rating_list = door_schedule["Fire Rating"].apply(lambda x: x if pd.notna(x) else "NA").to_list()

        item_description = BOQ_ALL[7:][[1, 2]]
        item_description = item_description.dropna()
        item_description.columns = item_description.iloc[0]
        item_description = item_description[1:].reset_index(drop=True)
        dicc_type_name = {}
        for i in range(len(item_description)):
            type_door = item_description.iloc[i, 0].strip() if item_description.iloc[i, 0].strip() != "Alt" else "ALT"
            name_door = item_description.iloc[i, 1].strip()
            dicc_type_name[type_door] = name_door
        door_type = door_schedule["Door Type"].to_list()
        namedoor_list = [dicc_type_name[x] if (x in dicc_type_name.keys()) else f"Door type {x} IS NOT FOUND" for x in door_type]

        hardware["Installed"] = ""
        hardware["Verified"] = ""
        hardware["Est hours"] = ""

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=LETTER)
        width, height = LETTER

        for i in range(len(namedoor_list)):
            y = height - inch
            left = 72
            y_footer = 0.75 * inch

            # Título centrado
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawCentredString(width / 2, y, str(project))
            y -= 30

            # Subtítulo
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(left, y, f"# {openings_list[i]}")
            y -= 20

            # Location + Fire Rating
            pdf.setFont("Helvetica", 8)
            pdf.drawString(left, y, f"Location: {location}")
            pdf.drawRightString(width - left, y, f"Fire Rating: {fire_rating_list[i]}")
            y -= 20

            # Building Area + Install Time
            pdf.drawString(left, y, f"Building Area: {building_area_list[i]}")
            pdf.drawRightString(width - left, y, f"Total Install Time: NA")
            y -= 30

            # Door y Frame con tamaños distintos
            pdf.setFont("Helvetica", 10)
            pdf.drawString(left, y, "Door: ")
            pdf.setFont("Helvetica", 8)
            pdf.drawString(left + 40, y, f"{namedoor_list[i]} (temporal name)")
            y -= 15

            pdf.setFont("Helvetica", 10)
            pdf.drawString(left, y, "Frame: ")
            pdf.setFont("Helvetica", 8)
            pdf.drawString(left + 42, y, f"{namedoor_list[i]} (temporal name)")
            y -= 15

            # Hardware Set
            pdf.setFont("Helvetica", 10)
            pdf.drawString(left, y, f"Hardware Set: {hardware_set_list_str[i]}")
            y -= 25

            # Línea separadora
            pdf.setStrokeColorRGB(0.7, 0.7, 0.7)
            pdf.line(left, y, width - left, y)
            y -= 15

            # Tabla hardware (más grande)
            group = f"GROUP NO. {hardware_set_list_str[i]}"
            filtered_hardware = hardware[hardware["HDW Group"] == group][columns_hardware]

            pdf.setFont("Courier", 11)
            for line in filtered_hardware.to_string(index=False).split("\n"):
                if y - 16 < y_footer + 40:
                    pdf.showPage()
                    y = height - inch
                    pdf.setFont("Courier", 11)

                pdf.drawString(0.5 * inch, y, line)
                y -= 14

            # Pie de página: Firma
            pdf.setFont("Helvetica", 10)
            pdf.drawString(left, y_footer, "Installed by: ____________________________")
            pdf.drawRightString(width - left, y_footer, "Date: ________________")

            pdf.showPage()

        pdf.save()
        buffer.seek(0)

    st.success("¡PDF generated successfully!")
    st.download_button(
        label="📥 Download PDF report",
        data=buffer,
        file_name=f"checklist_report_{project}.pdf",
        mime="application/pdf"
    )
else:
    st.info("📌 Please upload an Excel file to get started.")

st.markdown('<p class="footer-text">Made with dedication by Luis</p>', unsafe_allow_html=True)
