import streamlit as st
import yfinance as yf
import plotly.graph_objects as fgo
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Analítica Financiera", layout="wide")
st.title("📊 Aplicación de Analítica Financiera: Series de Tiempo")

# --- BARRA LATERAL (INPUTS DEL USUARIO) ---
st.sidebar.header("Configuración del Activo")

# 1. Casilla para colocar el Ticker
ticker_input = st.sidebar.text_input("Introduce el o los Tickers (ej: AMZN, NFLX, IBM, SPY):", "AMZN, NFLX, IBM, SPY")

# Procesar los tickers ingresados por el usuario
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

# 2. Selector de periodo de tiempo
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Fecha de inicio:", datetime(2014, 1, 1))
with col2:
    end_date = st.date_input("Fecha de fin:", datetime(2020, 7, 1))

# --- DESCARGA DE DATOS ---
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = True

if st.sidebar.button("Cargar Datos"):
    st.session_state.data_loaded = True

if st.session_state.data_loaded and tickers:
    try:
        with st.spinner("Descargando datos desde Yahoo Finance..."):
            # group_by='column' asegura una estructura más fácil de manipular
            datos = yf.download(tickers, start=start_date, end=end_date, group_by='column')
        
        if datos.empty:
            st.error("No se encontraron datos para los tickers o el rango de fechas seleccionado.")
        else:
            # --- SECCIÓN DE PRECIOS Y VOLÚMENES ---
            st.subheader("📈 Precios de Cierre y Volúmenes")
            
            # Extraer Precios y Volúmenes controlando si es uno o varios tickers
            if len(tickers) == 1:
                precios = datos['Close'].to_frame(name=tickers[0])
                volumen = datos['Volume'].to_frame(name=tickers[0])
            else:
                precios = datos['Close']
                volumen = datos['Volume']

            # Crear pestañas para organizar los gráficos
            tab1, tab2, tab3 = st.tabs(["Precios de Cierre", "Volúmenes", "Últimos Datos"])
            
            with tab1:
                fig_precios = fgo.Figure()
                for ticker in tickers:
                    if ticker in precios.columns:
                        fig_precios.add_trace(fgo.Scatter(x=precios.index, y=precios[ticker], name=ticker, mode='lines'))
                fig_precios.update_layout(title="Evolución de Precios de Cierre", xaxis_title="Fecha", yaxis_title="Precio", hovermode="x unified")
                st.plotly_chart(fig_precios, use_container_width=True)
                
            with tab2:
                fig_vol = fgo.Figure()
                for ticker in tickers:
                    if ticker in volumen.columns:
                        fig_vol.add_trace(fgo.Bar(x=volumen.index, y=volumen[ticker], name=ticker))
                fig_vol.update_layout(title="Volumen de Transacciones", xaxis_title="Fecha", yaxis_title="Volumen", barmode='group')
                st.plotly_chart(fig_vol, use_container_width=True)

            with tab3:
                st.write("Últimos 5 registros (redondeados a 3 decimales):")
                # Selección limpia de las columnas de Cierre y Volumen para mostrar
                columnas_validas = []
                if len(tickers) == 1:
                    df_mostrar = datos[['Close', 'Volume']].tail(5).round(3)
                else:
                    # Filtramos el dataframe para mostrar solo Close y Volume de forma ordenada
                    df_mostrar = datos.loc[:, datos.columns.get_level_values(0).isin(['Close', 'Volume'])].tail(5).round(3)
                st.dataframe(df_mostrar, use_container_width=True)

            # --- SECCIÓN TRANSVERSAL (CROSS SECTIONAL - HISTOGRAMAS) ---
            st.markdown("---")
            st.subheader("📊 Análisis de Distribución (Datos Transversales)")
            
            # Selector para elegir cuál de los tickers ingresados analizar
            ticker_hist = st.selectbox("Selecciona un ticker para ver su distribución:", tickers)
            
            precios_hist = precios[ticker_hist]
            
            año_inicio = start_date.year
            año_fin = end_date.year
            
            col_hist1, col_hist2 = st.columns(2)
            
            with col_hist1:
                datos_año1 = precios_hist[precios_hist.index.year == año_inicio].dropna()
                if not datos_año1.empty:
                    fig_h1 = fgo.Figure()
                    fig_h1.add_trace(fgo.Histogram(x=datos_año1, nbinsx=30, marker_color='gold', opacity=0.7, name=f"Precios {año_inicio}"))
                    fig_h1.update_layout(title=f"Densidad de Precios {ticker_hist} en {año_inicio}", xaxis_title="Precio Cierre", yaxis_title="Frecuencia")
                    st.plotly_chart(fig_h1, use_container_width=True)
                else:
                    st.warning(f"No hay datos suficientes para el año {año_inicio}")
                    
            with col_hist2:
                datos_año2 = precios_hist[precios_hist.index.year == año_fin].dropna()
                if not datos_año2.empty:
                    fig_h2 = fgo.Figure()
                    fig_h2.add_trace(fgo.Histogram(x=datos_año2, nbinsx=30, marker_color='blue', opacity=0.7, name=f"Precios {año_fin}"))
                    fig_h2.update_layout(title=f"Densidad de Precios {ticker_hist} en {año_fin}", xaxis_title="Precio Cierre", yaxis_title="Frecuencia")
                    st.plotly_chart(fig_h2, use_container_width=True)
                else:
                    st.warning(f"No hay datos suficientes para el año {año_fin}")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar los datos: {e}")
