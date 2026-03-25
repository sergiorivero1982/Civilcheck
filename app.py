import streamlit as st
import math

st.set_page_config(page_title="CivilCheck Pro - Bolivia", page_icon="🏗️", layout="centered")

st.title("🏗️ CivilCheck Pro: Verificación en Obra")
st.caption("Conforme a la Norma Boliviana NB 1225001 y ACI 318")
st.markdown("---")

# Menú lateral
menu = ["Vigas y Nervios", "Losas", "Columnas", "Zapatas Aisladas", "Muros de Contención", "Módulo de Acero"]
choice = st.sidebar.radio("Navegación", menu)

# --- FIRMA DEL AUTOR ---
st.sidebar.markdown("---")
st.sidebar.info("👨‍💻 Desarrollado por:\n\n**Ing. Sergio Rivero**")
# -----------------------

if choice == "Vigas y Nervios":
    st.header("📏 Pre-dimensionamiento de Vigas")
    L = st.number_input("Luz libre del tramo (metros)", min_value=0.5, value=5.0, step=0.1)
    condicion = st.selectbox("Condición de apoyo", 
                             ["Simplemente apoyada", "Un extremo continuo", "Ambos extremos continuos", "Voladizo"])
    
    coef_vigas = {"Simplemente apoyada": 16, "Un extremo continuo": 18.5, "Ambos extremos continuos": 21, "Voladizo": 8}
    coeficiente = coef_vigas[condicion]
    
    h = L / coeficiente
    b = h / 2
    deflexion_max = (L * 100) / 300 
    
    st.info(f"Criterio NB 1225001 (Cap. 9): L / {coeficiente}")
    st.success(f"Peralte mínimo recomendado (h): **{math.ceil(h*100)} cm**")
    st.info(f"Ancho sugerido (b): **{math.ceil(b*100)} cm**")
    st.warning(f"Deflexión máxima permisible (L/300): **{round(deflexion_max, 2)} cm**")

elif choice == "Losas":
    st.header("📐 Pre-dimensionamiento de Losas")
    tipo_losa = st.selectbox("Tipo de Losa", [
        "Losa Maciza (1 Dirección)", 
        "Losa Alivianada con Viguetas (1 Dirección)", 
        "Losa Reticular / Casetonada (2 Direcciones)"
    ])
    
    if tipo_losa == "Losa Maciza (1 Dirección)" or tipo_losa == "Losa Alivianada con Viguetas (1 Dirección)":
        L = st.number_input("Luz libre del tramo (metros)", min_value=0.5, value=4.0, step=0.1)
        condicion = st.selectbox("Condición de apoyo", 
                                 ["Simplemente apoyada", "Un extremo continuo", "Ambos extremos continuos", "Voladizo"])
        
        if tipo_losa == "Losa Maciza (1 Dirección)":
            coef_losas = {"Simplemente apoyada": 20, "Un extremo continuo": 24, "Ambos extremos continuos": 28, "Voladizo": 10}
            cap_norma = "(Cap. 7)"
        else:
            coef_losas = {"Simplemente apoyada": 16, "Un extremo continuo": 18.5, "Ambos extremos continuos": 21, "Voladizo": 8}
            cap_norma = "(Cap. 9 - Nervios)"
            
        coeficiente_losa = coef_losas[condicion]
        h = L / coeficiente_losa
        
        st.info(f"Criterio NB 1225001 {cap_norma}: L / {coeficiente_losa}")
        st.success(f"Espesor total mínimo de la losa (h): **{math.ceil(h*100)} cm**")
    else:
        L_mayor = st.number_input("Luz libre MAYOR del paño (metros)", min_value=2.0, value=6.0, step=0.1)
        condicion_2dir = st.selectbox("Ubicación del paño", [
            "Paño Exterior (sin viga de borde rígida)", 
            "Paño Exterior (con viga de borde)", 
            "Paño Interior"
        ])
        coef_reticular = {"Paño Exterior (sin viga de borde rígida)": 24, "Paño Exterior (con viga de borde)": 28, "Paño Interior": 30}
        coeficiente_ret = coef_reticular[condicion_2dir]
        h_ret = L_mayor / coeficiente_ret
        
        st.info(f"Criterio práctico: L / {coeficiente_ret}")
        st.success(f"Peralte total recomendado (h): **{math.ceil(h_ret*100)} cm**")

elif choice == "Columnas":
    st.header("🏢 Pre-dimensionamiento de Columnas")
    at = st.number_input("Área Tributaria (m2)", min_value=1.0, value=25.0, step=1.0)
    n = st.number_input("Número de pisos", min_value=1, value=5, step=1)
    fc = st.selectbox("Resistencia f'c (kg/cm2)", [210, 250, 280, 350])
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
    st.success(f"Carga Estimada de Servicio: **{P/1000:,.1f} Toneladas**")
    st.info(f"Sección cuadrada sugerida: **{math.ceil(lado)} x {math.ceil(lado)} cm**")

elif choice == "Zapatas Aisladas":
    st.header("🦶 Cimiento: Zapata Aislada")
    carga_ton = st.number_input("Carga total de la columna (Ton)", min_value=1.0, value=50.0, step=1.0)
    q_adm = st.number_input("Capacidad admisible del suelo (kg/cm2)", min_value=0.1, value=2.0, step=0.1)
    
    q_adm_ton_m2 = q_adm * 10
    area_zap = (carga_ton * 1.1) / q_adm_ton_m2
    lado_z = math.sqrt(area_zap)
    st.success(f"Área necesaria de desplante: **{round(area_zap, 2)} m2**")
    st.info(f"Lado sugerido para zapata cuadrada: **{math.ceil(lado_z * 100) / 100} m**")

elif choice == "Muros de Contención":
    st.header("🧱 Muro de Contención en Voladizo")
    
    col1, col2 = st.columns(2)
    with col1:
        H = st.number_input("Altura total del muro (H) [m]", min_value=1.0, value=3.0, step=0.1)
        B = st.number_input("Ancho de la base propuesto (B) [m]", min_value=0.5, value=2.0, step=0.1)
    with col2:
        gamma_s = st.number_input("Peso esp. Suelo (t/m3)", min_value=1.0, value=1.8, step=0.1)
        phi = st.number_input("Ángulo fricción suelo (grados)", min_value=15, value=30, step=1)
        q_adm = st.number_input("q admisible (kg/cm2)", min_value=0.1, value=2.0, step=0.1)
    
    st.markdown("### 1️⃣ Pre-dimensionamiento Recomendado")
    st.info(f"Ancho de base (B) sugerido: **{round(0.5*H, 2)} m a {round(0.7*H, 2)} m**")
    
    ka = (math.tan(math.radians(45 - phi/2)))**2
    Ea = 0.5 * gamma_s * (H**2) * ka
    M_volteo = Ea * (H / 3)
    
    W_total = B * H * 2.0 
    M_estab = W_total * (B / 2)
    
    FS_volteo = M_estab / M_volteo
    mu = math.tan(math.radians((2/3) * phi))
    FS_deslizamiento = (W_total * mu) / Ea
    
    st.markdown("### 2️⃣ Verificación de Estabilidad")
    st.write(f"- Empuje Activo (Ea): **{round(Ea, 2)} ton/m**")
    
    if FS_volteo >= 2.0:
        st.success(f"✅ FS Volteo: **{round(FS_volteo, 2)}** (Cumple mayor o igual a 2.0)")
    else:
        st.error(f"❌ FS Volteo: **{round(FS_volteo, 2)}** (Falla, requiere mayor base)")
        
    if FS_deslizamiento >= 1.5:
        st.success(f"✅ FS Deslizamiento: **{round(FS_deslizamiento, 2)}** (Cumple mayor o igual a 1.5)")
    else:
        st.error(f"❌ FS Deslizamiento: **{round(FS_deslizamiento, 2)}** (Falla, requiere mayor base)")

    st.markdown("### 3️⃣ Presiones en el Terreno")
    x_act = (M_estab - M_volteo) / W_total
    excentricidad = (B / 2) - x_act
    
    if excentricidad <= (B / 6):
        q_max_ton = (W_total / B) * (1 + (6 * excentricidad) / B)
        q_max_kg = q_max_ton / 10 
        if q_max_kg <= q_adm:
            st.success(f"✅ q_max: **{round(q_max_kg, 2)} kg/cm2** (Cumple menor a {q_adm})")
        else:
            st.error(f"❌ q_max: **{round(q_max_kg, 2)} kg/cm2** (Excede {q_adm}, ensanchar base)")
    else:
        st.warning("⚠️ La resultante cae fuera del tercio central (¡Peligro de levantamiento!)")

elif choice == "Módulo de Acero":
    st.header("⚙️ Gestión y Cuantía de Acero")
    barras = {"Ø 6 mm": [0.28, 0.222], "Ø 8 mm": [0.50, 0.395], "Ø 10 mm": [0.79, 0.617], 
              "Ø 12 mm": [1.13, 0.888], "Ø 16 mm": [2.01, 1.578], "Ø 20 mm": [3.14, 2.466], "Ø 25 mm": [4.91, 3.853]}
    tab1, tab2 = st.tabs(["Cálculo por Área", "Equivalencia de Barras"])
    
    with tab1:
        st.subheader("1️⃣ Varillas necesarias según el cálculo")
        area_req = st.number_input("Área de acero requerida (cm2)", min_value=0.1, value=10.0, step=0.1)
        for diametro, datos in barras.items():
            cantidad = math.ceil(area_req / datos[0])
            st.write(f"- **{cantidad} varillas de {diametro}** | Provee: **{round(cantidad * datos[0], 2)} cm2** | Peso: **{round(cantidad * datos[1], 2)} kg/m**")
            
    with tab2:
        st.subheader("2️⃣ Cambio de Diámetros en Obra")
        col1, col2 = st.columns(2)
        with col1: cant_actual = st.number_input("Cantidad de barras", min_value=1, value=4, step=1)
        with col2: diam_actual = st.selectbox("Diámetro en planos", list(barras.keys()), index=4) 
        
        area_actual = cant_actual * barras[diam_actual][0]
        peso_actual = cant_actual * barras[diam_actual][1]
        st.info(f"Acero de diseño: **{area_actual:.2f} cm2** | Peso lineal: **{peso_actual:.2f} kg/m**")
        
        st.markdown("### 🔄 Alternativas de armado:")
        for diametro, datos in barras.items():
            if diametro != diam_actual:
                cant_equiv = math.ceil(area_actual / datos[0])
                dif_peso = (cant_equiv * datos[1]) - peso_actual
                txt_peso = f"(+{dif_peso:.2f} kg/m extra)" if dif_peso > 0 else f"({dif_peso:.2f} kg/m ahorro)"
                st.write(f"- Usar **{cant_equiv} de {diametro}** | Provee: **{cant_equiv * datos[0]:.2f} cm2** | {txt_peso}")
