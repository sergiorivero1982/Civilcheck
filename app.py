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
       

elif choice == "Columnas (Carga Axial)":
    st.header("🏢 Pre-dimensionamiento de Columnas")
    st.write("Criterio por área tributaria y carga de servicio.")
    
    at = st.number_input("Área Tributaria ($m^2$)", min_value=1.0, value=25.0)
    n = st.number_input("Número de pisos", min_value=1, value=5)
    fc = st.selectbox("Resistencia f'c ($kg/cm^2$)", [210, 250, 280, 350])
    tipo = st.selectbox("Ubicación de columna", ["Central", "Extrema/Esquina"])
    
    # Carga estimada: 1000 kg/m2 por piso (Sencillo y conservador)
    P = 1000 * at * n
    # Factores de eficiencia según posición
    n_factor = 0.45 if tipo == "Central" else 0.35
    
    area_col = P / (n_factor * fc)
    lado = math.sqrt(area_col)
    
    st.success(f"Carga Total Estimada: **{P/1000:,.1f} Toneladas**")
    st.info(f"Sección requerida: **{math.ceil(lado)} x {math.ceil(lado)} cm**")

elif choice == "Zapatas Aisladas":
    st.header("🦶 Cimiento: Zapata Aislada")
    st.write("Estimación rápida del área de desplante.")
    
    carga_ton = st.number_input("Carga total de la columna (Toneladas)", min_value=1.0, value=50.0)
    q_adm = st.number_input("Capacidad admisible del suelo ($kg/cm^2$)", min_value=0.1, value=2.0)
    
    # Área = (P * 1.1) / q_adm  (El 1.1 es por peso propio de la zapata)
    area_zap = (carga_ton * 1000 * 1.1) / q_adm
    lado_z = math.sqrt(area_zap)
    
    st.success(f"Área necesaria: **{round(area_zap/10000, 2)} $m^2$**")
    st.info(f"Lado de zapata cuadrada: **{math.ceil(lado_z)} cm**")
