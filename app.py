import streamlit as st
import math

st.set_page_config(page_title="CivilCheck Pro", page_icon="🏗️", layout="centered")

st.title("🏗️ CivilCheck Pro: Verificación en Obra")
st.markdown("---")

# Menú actualizado
menu = ["Vigas y Nervios", "Losas Macizas (1 Dir)", "Columnas", "Zapatas Aisladas", "Módulo de Acero"]
choice = st.sidebar.radio("Navegación", menu)

if choice == "Vigas y Nervios":
    st.header("📏 Pre-dimensionamiento de Vigas")
    L = st.number_input("Luz libre del tramo (metros)", min_value=0.5, value=5.0, step=0.1)
    condicion = st.selectbox("Condición de apoyo", 
                             ["Simplemente apoyada", "Un extremo continuo", "Ambos extremos continuos", "Voladizo"])
    
    coef_vigas = {"Simplemente apoyada": 16, "Un extremo continuo": 18.5, "Ambos extremos continuos": 21, "Voladizo": 8}
    h = L / coef_vigas[condicion]
    b = h / 2
    deflexion_max = (L * 100) / 300 
    
    st.success(f"Peralte mínimo recomendado ($h$): **{math.ceil(h*100)} cm**")
    st.info(f"Ancho sugerido ($b$): **{math.ceil(b*100)} cm**")
    st.warning(f"Deflexión máxima permisible ($L/300$): **{round(deflexion_max, 2)} cm**")

elif choice == "Losas Macizas (1 Dir)":
    st.header("📐 Espesor de Losa Maciza")
    L = st.number_input("Luz libre del tramo (metros)", min_value=0.5, value=4.0, step=0.1)
    condicion = st.selectbox("Condición de apoyo", 
                             ["Simplemente apoyada", "Un extremo continuo", "Ambos extremos continuos", "Voladizo"])
    
    coef_losas = {"Simplemente apoyada": 20, "Un extremo continuo": 24, "Ambos extremos continuos": 28, "Voladizo": 10}
    h = L / coef_losas[condicion]
    st.success(f"Espesor mínimo de losa ($h$): **{math.ceil(h*100)} cm**")

elif choice == "Columnas":
    st.header("🏢 Pre-dimensionamiento de Columnas")
    at = st.number_input("Área Tributaria ($m^2$)", min_value=1.0, value=25.0, step=1.0)
    n = st.number_input("Número de pisos", min_value=1, value=5, step=1)
    fc = st.selectbox("Resistencia f'c ($kg/cm^2$)", [210, 250, 280, 350])
    tipo = st.selectbox("Ubicación de columna", ["Central", "Lateral", "Esquina"])
    
    P = 1000 * at * n
    if tipo == "Central":
        n_factor = 0.45
    elif tipo == "Lateral":
        n_factor = 0.35
    else: 
        n_factor = 0.30
        
    area_col = P / (n_factor * fc)
    lado = math.sqrt(area_col)
    
    st.success(f"Carga Total Estimada de Servicio: **{P/1000:,.1f} Toneladas**")
    st.info(f"Sección cuadrada sugerida: **{math.ceil(lado)} x {math.ceil(lado)} cm**")

elif choice == "Zapatas Aisladas":
    st.header("🦶 Cimiento: Zapata Aislada")
    carga_ton = st.number_input("Carga total de la columna (Ton)", min_value=1.0, value=50.0, step=1.0)
    q_adm = st.number_input("Capacidad admisible del suelo ($kg/cm^2$)", min_value=0.1, value=2.0, step=0.1)
    
    q_adm_ton_m2 = q_adm * 10
    area_zap = (carga_ton * 1.1) / q_adm_ton_m2
    lado_z = math.sqrt(area_zap)
    
    st.success(f"Área necesaria de desplante: **{round(area_zap, 2)} $m^2$**")
    st.info(f"Lado sugerido para zapata cuadrada: **{math.ceil(lado_z * 100) / 100} m**")

elif choice == "Módulo de Acero":
    st.header("⚙️ Gestión y Cuantía de Acero")
    
    # Diccionario con [Area (cm2), Peso Lineal (kg/m)]
    barras = {
        "Ø 6 mm": [0.28, 0.222],
        "Ø 8 mm": [0.50, 0.395],
        "Ø 10 mm": [0.79, 0.617],
        "Ø 12 mm": [1.13, 0.888],
        "Ø 16 mm": [2.01, 1.578],
        "Ø 20 mm": [3.14, 2.466],
        "Ø 25 mm": [4.91, 3.853]
    }
    
    tab1, tab2 = st.tabs(["Cálculo por Área", "Equivalencia de Barras"])
    
    with tab1:
        st.subheader("1️⃣ Varillas necesarias según el cálculo")
        area_req = st.number_input("Área de acero requerida ($cm^2$)", min_value=0.1, value=10.0, step=0.1)
        
        for diametro, datos in barras.items():
            area_barra = datos[0]
            peso_lineal = datos[1]
            cantidad = math.ceil(area_req / area_barra)
            area_provista = cantidad * area_barra
            peso_total = cantidad * peso_lineal
            
            st.write(f"- **{cantidad} varillas de {diametro}** | Provee: **{round(area_provista, 2)} $cm^2$** | Peso: **{round(peso_total, 2)} kg/m**")
            
    with tab2:
        st.subheader("2️⃣ Cambio de Diámetros en Obra")
        col1, col2 = st.columns(2)
        with col1:
            cant_actual = st.number_input("Cantidad de barras", min_value=1, value=4, step=1)
        with col2:
            diam_actual = st.selectbox("Diámetro en planos", list(barras.keys()), index=4) # 16mm por defecto, índice ajustado por el 6mm
        
        area_actual = cant_actual * barras[diam_actual][0]
        peso_actual = cant_actual * barras[diam_actual][1]
        
        st.info(f"Acero de diseño: **{area_actual:.2f} $cm^2$** | Peso lineal: **{peso_actual:.2f} kg/m**")
        
        st.markdown("### 🔄 Alternativas de armado:")
        st.caption("Garantizando un área igual o mayor a la de diseño.")
        for diametro, datos in barras.items():
            if diametro != diam_actual:
                area_barra = datos[0]
                peso_lineal = datos[1]
                cant_equiv = math.ceil(area_actual / area_barra)
                area_provista = cant_equiv * area_barra
                peso_nuevo = cant_equiv * peso_lineal
                
                # Para ver si el cambio nos suma muchos kilos al presupuesto
                dif_peso = peso_nuevo - peso_actual
                if dif_peso > 0:
                    txt_peso = f"(+{dif_peso:.2f} kg/m extra)"
                else:
                    txt_peso = f"({dif_peso:.2f} kg/m ahorro)"
                    
                st.write(f"- Usar **{cant_equiv} de {diametro}** | Provee: **{area_provista:.2f} $cm^2$** | {txt_peso}")
