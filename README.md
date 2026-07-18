# 📊 Aplicación de Analítica Financiera Universal

Esta es una aplicación interactiva desarrollada en **Python** utilizando **Streamlit**, diseñada para la descarga, visualización y análisis de activos financieros de manera universal. Permite transformar análisis tradicionales en un entorno web dinámico y accesible.

La aplicación está inspirada en un ejercicio original de analítica financiera estructurado en R (utilizando `quantmod` y `dygraphs`), migrando toda la lógica al ecosistema de Python para ofrecer una interfaz de usuario flexible y moderna.

## 🚀 Características

- **Búsqueda Universal de Tickers:** Permite ingresar cualquier símbolo válido de Yahoo Finance (acciones globales, índices, criptomonedas, etc.), ya sea de forma individual o múltiple separados por comas.
- **Selectores Temporales Interactivos:** Casillas dinámicas para definir el período exacto de análisis (fecha de inicio y fin).
- **Gráficos Dinámicos (Series de Tiempo):** Visualización interactiva de los Precios de Cierre y Volúmenes diarios mediante pestañas, impulsada por `Plotly`.
- **Análisis Transversal (Cross-Sectional):** Histogramas inteligentes que comparan automáticamente la distribución y densidad de precios entre el primer y el último año del rango seleccionado.

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**
- **Streamlit:** Para el desarrollo de la interfaz web interactiva.
- **yfinance:** Para la extracción de datos financieros en tiempo real desde Yahoo Finance.
- **Plotly:** Para la generación de gráficos interactivos y profesionales.
- **Pandas:** Para la manipulación, limpieza y estructuración de los datos.

## 📦 Instalación Local

Si deseas ejecutar este proyecto en tu entorno local, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
   cd TU_REPOSITORIO
