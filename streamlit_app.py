import streamlit as st
import pandas as pd
from PIL import Image

# Cargar logo
logo = Image.open("logo_para_app.png")
st.image(logo, use_column_width=True)

# Título
st.title("CALCULADORA MARTINEZ/ITALIANO")
st.subheader("Comparación de movilidad según ANSeS vs Justicia")

# Inputs
caso = st.text_input("Nombre del caso")
haber_base = st.text_input("Ingrese el haber base")
fecha_base = st.text_input("Fecha del haber base (YYYY-MM)")

# Validar y procesar si se completaron los datos
if haber_base and fecha_base:
    try:
        haber_base = float(haber_base.replace(",", "."))  # convertir a número

        df_anses = pd.read_csv("movilidad_anses.csv", sep=",")
        df_justicia = pd.read_csv("movilidad_martinez_italiano.csv", sep=",")

        df_anses["fecha"] = pd.to_datetime(df_anses["fecha"], format="%Y-%m")
        df_justicia["fecha"] = pd.to_datetime(df_justicia["fecha"], format="%Y-%m")
        df_anses["coeficiente_anses"] = df_anses["coeficiente_anses"].astype(float)
        df_justicia["coeficiente_justicia"] = df_justicia["coeficiente_justicia"].astype(float)

        fecha_base_dt = pd.to_datetime(fecha_base, format="%Y-%m")
        coef_anses = df_anses[df_anses["fecha"] > fecha_base_dt]["coeficiente_anses"]
        coef_justicia = df_justicia[df_justicia["fecha"] > fecha_base_dt]["coeficiente_justicia"]

        haber_anses = haber_base
        for coef in coef_anses:
            haber_anses *= coef

        haber_justicia = haber_base
        for coef in coef_justicia:
            haber_justicia *= coef

        diferencia = haber_justicia - haber_anses
        porcentaje = (diferencia / haber_anses) * 100

        st.markdown("### Resultados:")
        st.markdown(f"**Caso:** {caso}")
        st.markdown(f"**Haber actualizado según ANSeS:** ${haber_anses:,.2f}")
        st.markdown(f"**Haber actualizado según Justicia:** ${haber_justicia:,.2f}")
        st.markdown(f"**Diferencia:** ${diferencia:,.2f} ({porcentaje:.2f}%)")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")