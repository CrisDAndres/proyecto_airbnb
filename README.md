# PROYECTO MÓDULO 2: DATASET AIRBNB ROMA

![Imagen]('./roma_ia.jpg') 
*Fuente de la imagen: Copilot Designer*

En este proyecto se explorará un conjunto de datos de las viviendas anunciadas en la plataforma Airbnb en esta ciudad de Italia. De esta manera, se analizará el impacto de Airbnb en el mercado de viviendas en una ciudad tan turística como Roma, y los patrones de alquiler, precios y flujos turísticos de la ciudad.

Este análisis permitirá comprender el impacto de esta plataforma y formular posibles regulaciones para abordar los problemas asociados.

Los datos con los que se trabajarán corresponden al registro de anuncios de Airbnb publicados en la ciudad de Roma a fecha del 15 de diciembre de 2023. 

### Características del proyecto

- Los datos de este proyecto se obtuvieron de la web https://insideairbnb.com/get-the-data/.
- El código empleado está en el notebook ``proyecto_airbnb.ipynb`` y contiene los siguientes apartados:
    - Carga de librerías y lectura de los diferentes dataset
    - Información de los dataset
    - Pre-procesamiento de los datos: reparación valores nulos y atípicos
    - Análisis exploratorio de los datos (EDA): Aquí se incluye la visualización de mapas interactivos y otros gráficos
    - Conclusiones
- Se ha empleado la plataforma de **Streamlit** para el desarrollo de una app interactiva que permite la exploración y visualización de los datos analizados: METER LINK

### Instrucciones de Ejecución 💻

Para ejecutar este proyecto en tu máquina local, sigue los siguientes pasos:

1. Clona este repositorio en tu máquina local.
2. Abre el notebook proyecto_airbnb_Roma.ipynb en Jupyter Notebook.
3. Ejecuta cada celda del notebook en orden para reproducir el análisis y los resultados.
4. Para la ejecución de la aplicación e Streamlit, asegúrate de tener instalado folium en streamlit (``pip install streamlit-folium``) y ejecuta el archivo app_airbnb.py con el siguiente comando: streamlit run app_airbnb.py
