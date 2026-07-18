import streamlit as st
import yfinance as yf
import plotly.graph_objects as fgo
import pandas as pd
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Analítica Financiera Universal", layout="wide")
st.title("📊 Aplicación de Analítica Financiera Universal")
st.write("Introduce cualquier ticker válido de Yahoo Finance para analizar sus series de tiempo.")

# --- BARRA LATERAL (INPUTS DEL USUARIO) ---
st.sidebar.header("Configuración del Activo")

# 1. Casilla libre para colocar CUALQUIER Ticker (Por defecto dejamos uno de ejemplo, pero se puede borrar todo)
ticker_input = st.sidebar.text_input(
    "Introduce los Tickers separados por coma (ej: AAPL, BTC-USD, TSLA, MSFT):", 
    "AAPL, MSFT"
)

# Procesar y limpiar los tickers ingresados por el usuario
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

# 2. Selector de periodo de tiempo libre
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Fecha de inicio:", datetime(2018, 1, 1))
with col2:
    end_date = st.date_input("Fecha de fin:", datetime(2025, 1, 1))

# --- DESCARGA Y PROCESAMIENTO DE DATOS ---
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = True

if st.sidebar.button("Actualizar / Cargar Datos"):
    st.session_state.data_loaded = True

if st.session_state.data_loaded and tickers:
    try:
        with st.spinner("Buscando y descargando datos en Yahoo Finance..."):
            
            # Descargamos los datos uno a uno para garantizar compatibilidad universal
            dict_precios = {}
            dict_volumen = {}
            
            for ticker in tickers:
                df_ticker = yf.download(ticker, start=start_date, end=end_date, progress=False)
                if not df_ticker.empty:
                    # Forzamos a que la serie sea plana (1D) extrayendo la columna 'Close' y 'Volume'
                    dict_precios[ticker] = df_ticker['Close'].squeeze()
                    dict_volumen[ticker] = df_ticker['Volume'].squeeze()
            
            # Creamos DataFrames limpios donde cada columna es un ticker
            df_precios = pd.DataFrame(dict_precios)
            df_volumen = pd.DataFrame(dict_volumen)

        if df_precios.empty:
            st.error("No se encontraron datos. Asegúrate de que los tickers estén bien escritos y existan en Yahoo Finance.")
        else:
            # --- SECCIÓN DE PRECIOS Y VOLÚMENES ---
            st.subheader("📈 Series de Tiempo: Precios y Volúmenes")
            
            # Crear pestañas para organizar los gráficos dinámicos
            tab1, tab2, tab3 = st.tabs(["Precios de Cierre", "Volúmenes de Transacción", "Historial de Datos"])
            
            with tab1:
                fig_precios = fgo.Figure()
                for ticker in df_precios.columns:
                    fig_precios.add_trace(fgo.Scatter(x=df_precios.index, y=df_precios[ticker], name=ticker, mode='lines'))
                fig_precios.update_layout(
                    title="Evolución de Precios de Cierre", 
                    xaxis_title="Fecha", 
                    yaxis_title="Precio (USD / Moneda local)", 
                    hovermode="x unified"
                )
                st.plotly_chart(fig_precios, use_container_width=True)
                
            with tab2:
                fig_vol = fgo.Figure()
                for ticker in df_volumen.columns:
                    fig_vol.add_trace(fgo.Bar(x=df_volumen.index, y=df_volumen[ticker], name=ticker))
                fig_vol.update_layout(
                    title="Volumen Diario de Transacciones", 
                    xaxis_title="Fecha", 
                    yaxis_title="Volumen", 
                    barmode='group'
                )
                st.plotly_chart(fig_vol, use_container_width=True)

            with tab3:
                st.write("Últimos 5 registros recuperados (Redondeados a 3 decimales):")
                # Creamos una tabla conjunta combinando Precio y Volumen de manera clara
                df_combinado = pd.DataFrame(index=df_precios.index)
                for ticker in df_precios.columns:
                    df_combinado[f"{ticker} P.Cierre"] = df_precios[ticker]
                    df_combinado[f"{ticker} Vol"] = df_volumen[ticker]
                
                st.dataframe(df_combinado.tail(5).round(3), use_container_width=True)

            # --- SECCIÓN TRANSVERSAL (HISTOGRAMAS DINÁMICOS) ---
            st.markdown("---")
            st.subheader("📊 Análisis de Distribución (Datos Transversales)")
            
            # Selector para elegir cuál de los tickers ingresados se quiere analizar detalladamente
            ticker_hist = st.selectbox("Selecciona qué activo deseas analizar de forma transversal:", df_precios.columns)
            
            serie_hist = df_precios[ticker_hist]
            
            # Detectar automáticamente los años disponibles basados en la selección del usuario
            años_disponibles = sorted(list(set(serie_hist.index.year)))
            
            if len(años_disponibles) >= 2:
                col_hist1, col_hist2 = st.columns(2)
                
                # Año inicial disponible en la selección
                año_inicio = años_disponibles[0]
                # Año final disponible en la selección
                año_fin = años_disponibles[-1]
                
                with col_hist1:
                    datos_año1 = serie_hist[serie_hist.index.year == año_inicio].dropna()
                    if not datos_año1.empty:
                        fig_h1 = fgo.Figure()
                        fig_h1.add_trace(fgo.Histogram(x=datos_año1, nbinsx=30, marker_color='gold', opacity=0.7))
                        fig_h1.update_layout(title=f"Distribución de {ticker_hist} en el año {año_inicio}", xaxis_title="Precio Cierre", yaxis_title="Frecuencia")
                        st.plotly_chart(fig_h1, use_container_width=True)
                        
                with col_hist2:
                    datos_año2 = serie_hist[serie_hist.index.year == año_fin].dropna()
                    if not datos_año2.empty:
                        fig_h2 = fgo.Figure()
                        fig_h2.add_trace(fgo.Histogram(x=datos_año2, nbinsx=30, marker_color='blue', opacity=0.7))
                        fig_h2.update_layout(title=f"Distribución de {ticker_hist} en el año {año_fin}", xaxis_title="Precio Cierre", yaxis_title="Frecuencia")
                        st.plotly_chart(fig_h2, use_container_width=True)
            else:
                st.info("Selecciona un rango de tiempo de al menos 2 años diferentes para habilitar la comparación de histogramas anuales.")

    except Exception as e:
        st.error(f"Error al procesar la solicitud: {e}. Asegúrate de introducir tickers válidos.")

