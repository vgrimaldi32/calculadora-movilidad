
import streamlit as st
import pandas as pd
from PIL import Image

# Logo
st.image("logo_para_app.png", width=200)

st.title("CALCULADORA MARTINEZ/ITALIANO")
st.subheader("Comparación de movilidad según ANSeS vs Justicia")

# Entradas
nombre = st.text_input("Nombre del caso")
haber = st.number_input("Ingrese el haber base", min_value=0.0, format="%.2f")
fecha_base = st.text_input("Fecha del haber base (YYYY-MM)", value="2020-01")

# Carga coeficientes
df_anses = pd.read_csv("movilidad_anses.csv")
df_justicia = pd.read_csv("movilidad_justicia.csv")
df_anses["fecha"] = pd.to_datetime(df_anses["fecha"], format="%Y-%m")
df_justicia["fecha"] = pd.to_datetime(df_justicia["fecha"], format="%Y-%m")
fecha_base_dt = pd.to_datetime(fecha_base, format="%Y-%m")

# Filtro desde la fecha base
coef_anses = df_anses[df_anses["fecha"] >= fecha_base_dt]["coef_anses"].astype(float)
coef_justicia = df_justicia[df_justicia["fecha"] >= fecha_base_dt]["coef_justicia"].astype(float)

# Cálculo de haberes actualizados
try:
    haber_anses = haber
    for c in coef_anses:
        haber_anses *= c

    haber_justicia = haber
    for c in coef_justicia:
        haber_justicia *= c

    diferencia = haber_justicia - haber_anses
    porcentaje = (diferencia / haber_anses) * 100 if haber_anses > 0 else 0

    # Resultados
    st.markdown("### Resultados:")
    st.markdown(f"**Caso:** {nombre}")
    st.markdown(f"**Haber actualizado según ANSeS:** ${haber_anses:,.2f}")
    st.markdown(f"**Haber actualizado según Justicia:** ${haber_justicia:,.2f}")
    st.markdown(f"**Diferencia:** ${diferencia:,.2f} ({porcentaje:.2f}%)")

except Exception as e:
    st.error(f"Ocurrió un error: {e}")
