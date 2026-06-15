import streamlit as st
import pandas as pd
import numpy as np

# Configuración de la página web estilo Gamer / Dark
st.set_page_config(page_title="SUPERCLÁSICO PES - Dashboard", layout="wide", initial_sidebar_state="expanded")

# Estilos CSS para sintonizar los colores de los equipos (Gris/Negro y Rojo)
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .metric-box { background-color: #1f2937; padding: 20px; border-radius: 10px; text-align: center; border-left: 5px solid #ff4b4b; }
    .vdg-box { background-color: #111827; padding: 15px; border-radius: 8px; border-top: 4px solid #4b5563; text-align: center; }
    .sdc-box { background-color: #111827; padding: 15px; border-radius: 8px; border-top: 4px solid #ef4444; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# Título principal de la App
st.title("⚽ SUPERCLÁSICO PES — Panel de Control")
st.caption("Historial unificado de temporadas, estadísticas de jugadores y carrera por el Balón de Oro")
st.write("---")

# Función optimizada para leer el Excel actual
@st.cache_data
def cargar_datos():
    archivo = "SUPERCLASICO PES.xlsx"
    df_hist = pd.read_excel(archivo, sheet_name="DATOS HISTÓRICOS", header=None)
    df_t1 = pd.read_excel(archivo, sheet_name="TEMPORADA 1", header=None)
    df_t2 = pd.read_excel(archivo, sheet_name="TEMPORADA 2", header=None)
    return df_hist, df_t1, df_t2

try:
    df_hist, df_t1, df_t2 = cargar_datos()
    
    # MARCADOR GLOBAL & PATERNIDAD
    triunfos_vdg = int(df_hist.iloc[11, 1])
    triunfos_sdc = int(df_hist.iloc[11, 4])
    empates = int(df_hist.iloc[13, 1])
    goles_vdg = int(df_hist.iloc[16, 1])
    goles_sdc = int(df_hist.iloc[16, 4])
    paternidad_texto = str(df_hist.iloc[18, 2])
    
    col1, col2, col3 = st.columns([2, 3, 2])
    
    with col1:
        st.markdown(f"<div class='vdg-box'><h3>🇩🇪 VIUDAS DE GALLARDO</h3><h1 style='color:#9ca3af;'>{triunfos_vdg}</h1><p>Triunfos Históricos</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1 style='text-align: center; font-size: 60px; margin: 0;'>{triunfos_vdg} - {triunfos_sdc}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: #ef4444; font-weight: bold;'>HISTORIAL A FAVOR DE: {paternidad_texto}</p>", unsafe_allow_html=True)
        
        total_partidos = triumphs_vdg = triunfos_vdg + triunfos_sdc + empates
        if total_partidos > 0:
            pct_vdg = triunfos_vdg / total_partidos
            pct_sdc = triunfos_sdc / total_partidos
            pct_emp = empates / total_partidos
            barra_data = pd.DataFrame([{
                'Viudas de Gallardo (🇩🇪)': pct_vdg, 
                'Empates (🤝)': pct_emp, 
                'Soldado de Coudet (⚪🔴)': pct_sdc
            }])
            st.bar_chart(barra_data, horizontal=True, color=["#4b5563", "#374151", "#ef4444"], height=130)
            
    with col3:
        st.markdown(f"<div class='sdc-box'><h3>⚪🔴 SOLDADO DE COUDET</h3><h1 style='color:#ef4444;'>{triunfos_sdc}</h1><p>Triunfos Históricos</p></div>", unsafe_allow_html=True)

    st.write("---")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Partidos Jugados 🎮", f"{total_partidos} partidos")
    m2.metric("Empates Registrados 🤝", f"{empates} empates")
    m3.metric("Goles Metidos por VDG ⚽", f"{goles_vdg} goles")
    m4.metric("Goles Metidos por SDC ⚽", f"{goles_sdc} goles")

    st.write("---")

    st.header("📊 Desempeño y Estadísticas de Equipos")
    vista = st.selectbox("Elegí la pestaña que querés analizar:", ["Estadísticas Históricas", "Temporada 1", "Temporada 2"])

    def procesar_tabla_jugadores(df):
        jugadores_vdg = df.iloc[3:36, [0, 1, 2, 3, 5, 6, 7]].dropna(subset=[0])
        jugadores_vdg.columns = ['Jugador', 'Goles', 'MVPs', 'Partidos', 'Rojas', 'Amarillas', 'Puntos PBDO']
        jugadores_vdg['Equipo'] = 'Viudas de Gallardo'
        
        jugadores_sdc = df.iloc[3:36, [11, 12, 13, 14, 15, 16, 17]].dropna(subset=[11])
        jugadores_sdc.columns = ['Jugador', 'Goles', 'MVPs', 'Partidos', 'Rojas', 'Amarillas', 'Puntos PBDO']
        jugadores_sdc['Equipo'] = 'Soldado de Coudet'
        
        return pd.concat([jugadores_vdg, jugadores_sdc], ignore_index=True)

    if vista == "Estadísticas Históricas":
        st.subheader("🏆 Máximos Goleadores de la Historia Completa")
        goleadores_hist = df_hist.iloc[2:12, [6, 7, 8]]
        goleadores_hist.columns = ['Jugador', 'Goles Totales', 'Equipo']
        st.dataframe(goleadores_hist, use_container_width=True, hide_index=True)

    else:
        df_act = df_t1 if vista == "Temporada 1" else df_t2
        tabla_completa = procesar_tabla_jugadores(df_act)
        
        for col in ['Goles', 'MVPs', 'Partidos', 'Rojas', 'Amarillas', 'Puntos PBDO']:
            tabla_completa[col] = pd.to_numeric(tabla_completa[col], errors='coerce').fillna(0).astype(int)

        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.subheader("🥇 Carrera por el Balón de Oro (Top de la Edición)")
            top_pbdo = tabla_completa[tabla_completa['Puntos PBDO'] > 0].sort_values(by='Puntos PBDO', ascending=False).head(5)
            st.dataframe(top_pbdo[['Jugador', 'Puntos PBDO', 'Equipo']], use_container_width=True, hide_index=True)
            
        with col_t2:
            st.subheader("🔥 Máximos Goleadores del Torneo")
            top_goles = tabla_completa[tabla_completa['Goles'] > 0].sort_values(by='Goles', ascending=False).head(5)
            st.dataframe(top_goles[['Jugador', 'Goles', 'Equipo']], use_container_width=True, hide_index=True)
            
        st.write("---")
        st.subheader("📋 Buscador General de Jugadores del Torneo")
        st.dataframe(tabla_completa, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"❌ Asegurate de subir el Excel con el nombre exacto 'SUPERCLASICO PES.xlsx' en la misma carpeta.")