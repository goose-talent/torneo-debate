from docxtpl import DocxTemplate
import mysql.connector
import os
import subprocess
import streamlit as st

conexion = mysql.connector.connect(
    host=st.secrets["MYSQL_HOST"],
    port=st.secrets["MYSQL_PORT"],
    user=st.secrets["MYSQL_USER"],
    password=st.secrets["MYSQL_PASSWORD"],
    database=st.secrets["MYSQL_DATABASE"]
)

cursor = conexion.cursor(dictionary=True)

os.makedirs("diplomas", exist_ok=True)

def convertir_pdf(ruta_docx, carpeta_salida):
    subprocess.run([
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", carpeta_salida,
        ruta_docx
    ])

cursor.execute("""
SELECT nombre, apellidos, centro
FROM debatientes
""")

debatientes = cursor.fetchall()

for p in debatientes:

   
    centro_limpio = p["centro"].replace("/", "-")
    carpeta_centro = f"diplomas/{centro_limpio}"

    os.makedirs(carpeta_centro, exist_ok=True)

    doc = DocxTemplate("DIPLOMA_DEBATIENTE.docx")

    
    context = {
        "nombre_apellido": f"{p['nombre']} {p['apellidos']}",
        "nombre_centro": p["centro"]
    }

    doc.render(context)

    nombre_archivo = f"diploma_{p['nombre']}_{p['apellidos']}.docx"
    ruta_docx = f"{carpeta_centro}/{nombre_archivo}"

   
    doc.save(ruta_docx)

   
    convertir_pdf(ruta_docx, carpeta_centro)


print("Diplomas PDF generados correctamente")