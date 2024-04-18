# Análisis del Impacto de Airbnb en el Mercado de Viviendas en Roma 🏛️

<p align="center">
  <img src="img/rome_prettymaps.png" alt="Logo">
</p>
<p align="center"><em>by prettymaps</em></p>

En este proyecto se explorará un conjunto de datos de las viviendas anunciadas en la plataforma Airbnb en la ciudad de Roma. De esta manera, se analizará el impacto de Airbnb en el mercado de viviendas en esta ciudad tan turística, patrones de alquiler, precios y flujos turísticos de la ciudad.

Este análisis permitirá comprender el impacto de esta plataforma y formular posibles regulaciones para abordar los problemas asociados.

Los datos con los que se trabajarán corresponden al registro de anuncios de Airbnb publicados en la ciudad de Roma a fecha del 15 de diciembre de 2023. 

### Características del proyecto

- **Datos**: Los datos de este proyecto se obtuvieron de la web [Inside Airbnb](https://insideairbnb.com/get-the-data/).
- **Código**: El código empleado se encuentra en el notebook ``proyecto_airbnb.ipynb`` e incluye los siguientes apartados:
    - Carga de librerías y lectura de los diferentes dataset.
    - Información de los dataset.
    - Pre-procesamiento de los datos: reparación valores nulos y atípicos.
    - Análisis exploratorio de los datos (EDA), incluyendo la visualización de mapas interactivos y otros gráficos.
    - Conclusiones.
- **Aplicación de Streamlit**: Se ha desarrollado una aplicación interactiva utilizando Streamlit, que permite la exploración y visualización de los datos analizados. Está desplegada en https://airbnb-rome.streamlit.app/

### Instrucciones de Ejecución 💻

Para ejecutar este proyecto en tu máquina local, sigue los siguientes pasos:

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias ejecutando ``pip install -r requirements.txt``.
3. Ejecuta el archivo ``app_airbnb.py`` y asegúrate de tener descargadas la carpetas ``data``, ``img`` y ``html`` en el mismo entorno. A continuación, abre el terminal en el directorio de la app y ejecuta el siguiente comando: ``streamlit run app_airbnb.py``.
4. Se abrirá en navegador web ``http://localhost:8501/`` que te llevará a la app.

### Análisis con Power BI 📊

Se ha realizado un análisis complementario utilizando Power BI, creando un panel interactivo para explorar y comprender los patrones y tendencias en los datos.
Este panel se encuentra dentro de la aplicación de Streamlit. 

### To do

[ ] Implementación de un modelo de machine learning para predecir los precios de los alojamientos en base a una serie de parámetros insertados. 
