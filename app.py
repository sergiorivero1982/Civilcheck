import streamlit as st
import math

st.set_page_config(page_title="CivilCheck Pro", page_icon="🏗️", layout="centered")

st.title("🏗️ CivilCheck Pro: Verificación en Obra")
st.markdown("---")

menu = ["Vigas y Nervios", "Losas Macizas (1 Dir)", "Cuantía de Acero"]
choice = st.sidebar.radio("Navegación", menu)

if choice == "Vigas y Nervios":
    st.header("📏 Pre-dimensionamiento de Vigas")
    L = st.number_input("Luz libre del tramo (metros)", min_value=0.5, value=5.0, step=0.1)
    condicion = st.selectbox("Condición de apoyo", 
                             ["Simplemente apoyada", "Un extremo continuo", "Ambos extremos continuos", "Voladizo"])
    
    # Coeficientes ACI 318 para vigas
    coef_vigas = {
        "Simplemente apoyada": 16, 
        "Un extremo continuo": 18.5, 
        "Ambos extremos continuos": 21, 
        "Voladizo": 8
    }
    
    h = L / coef_vigas[condicion]
    b = h / 2  # Regla práctica inicial para el ancho
    
    st.success(f"Peralte mínimo recomendado ($h$): **{math.ceil(h*100)} cm**")
    st.info(f"Ancho sugerido ($b$): **{math.ceil(b*100)} cm**")
    st.caption("Nota: El ancho $b$ suele ajustarse a múltiplos de 5 cm (ej. 20, 25, 30 cm) por modulación de encofrados.")

elif choice == "Losas Macizas (1 Dir)":
    st.header("📐 Espesor de Losa Maciza")
    L = st.number_input("Luz libre del tramo (metros)", min_value=0.5, value=4.0, step=0.1)
    condicion = st.selectbox("Condición de apoyo", 
                             ["Simplemente apoyada", "Un extremo continuo", "Ambos extremos continuos", "Voladizo"])
    
    # Coeficientes ACI 318 para losas macizas
    coef_losas = {
        "Simplemente apoyada": 20, 
        "Un extremo continuo": 24, 
        "Ambos extremos continuos": 28, 
        "Voladizo": 10
    }
    
    h = L / coef_losas[condicion]
    st.success(f"Espesor mínimo de losa ($h$): **{math.ceil(h*100)} cm**")

elif choice == "Cuantía de Acero":
    st.header("⚙️ Verificación de Armadura")
    st.write("Calcula cuántas varillas necesitas para cubrir un área de acero dada por el cálculo.")
    
    area_req = st.number_input("Área de acero requerida ($cm^2$)", min_value=0.1, value=10.0, step=0.1)
    
    # Áreas de varillas comerciales en cm2
    barras = {
        "Ø 10 mm": 0.79,
        "Ø 12 mm": 1.13,
        "Ø 16 mm": 2.01,
        "Ø 20 mm": 3.14,
        "Ø 25 mm": 4.91
    }
    
    st.markdown("### Opciones de armado:")
    for diametro, area_barra in barras.items():
        cantidad = math.ceil(area_req / area_barra)
        area_provista = cantidad * area_barra
        st.write(f"- **{cantidad} varillas de {diametro}** (Provee {round(area_provista, 2)} $cm^2$)")
