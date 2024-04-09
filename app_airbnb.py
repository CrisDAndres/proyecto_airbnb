# ---------------------LIBRERÍAS----------------------#
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import warnings
from pandas.errors import SettingWithCopyWarning
# Gráficas
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
import plotly.graph_objects as go
# Mapas interactivos
import folium
from folium import plugins
from folium.plugins import FastMarkerCluster
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
# Nube de palabras
from PIL import Image 


warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))
 

# ---------------------CONFIGURACIÓN DE LA PÁGINA----------------------#
st.set_page_config(
    page_title="Airbnb: Roma",
    page_icon="🏛️",
    layout="wide", # Esta opción busca el tam de la pantalla, y de izq a dcha va a intentar que el contenido ocupe el mayor espacio posible
    initial_sidebar_state="expanded", # o collapsed
)

# ---------------------COSAS QUE VAMOS A USAR EN LA APP----------------------#

# Función para cargar los datos, mantener los datos cargados
# y evitar recargas innecesarias que puedan reiniciar la aplicación.
@st.cache_data()
def load_data():
    df_nopreproc = pd.read_csv("data/airbnb_nopreproc.csv") # Antes de cualquier preprocesamiento, solo con algunas columnas elegidas
    df_preproc1 = pd.read_csv("data/airbnb_preproc1.csv") # Antes de reparar los outliers
    df = pd.read_csv("data/airbnb_limpio.csv")
    geo_final = pd.read_csv("data/geo_final.csv") 
    return df_nopreproc, df_preproc1, df, geo_final

# Carga de datos
df_nopreproc, df_preproc1, df, geo_final = load_data()

# Imágenes
logo = "img/logorome.png" 
image = "img/rome_ia.jpg"


# ---------------------HEADER----------------------#
st.image(image, caption = 'Imagen generada por IA', width=250)
st.title("Análisis de los alojamientos de Airbnb en Roma")
st.write('🏛️ ¡Explora esta maravillosa ciudad!')


# ---------------------SIDEBAR----------------------#

st.sidebar.image(logo,width=250) 
st.sidebar.title("ÍNDICE")

# Mejora: Mantener el estado de la selección actual en la barra lateral para evitar reinicios
page_options = ["Introducción", "Preprocesamiento", "Análisis exploratorio"]
page = st.sidebar.radio("Seleccione la página:", page_options, index=0, key='current_page')

page_options = ["Introducción", "Preprocesamiento", "Análisis exploratorio"]


# ---------------------BODY----------------------#

# PÁGINA 1-------------------------------------
if page == "Introducción":
    
    st.markdown("""
                ***Roma, la ciudad eterna, ha sido el punto de encuentro de diferentes culturas y religiones con una historia que se remonta a más de dos milenios.
                Ubicada en la región de Lazio, Roma es la capital del país y la ciudad más grande de la península de Italia.
                Hoy en día es una metrópolis vibrante que combina la grandeza de su pasado con la vitalidad de una ciudad moderna, que atrae a millones de turistas cada año.***
                """)

    st.markdown("""
             *En este contexto, el mercado de alojamientos de Airbnb en Roma desempeña un papel importante, brindando a los visitantes la oportunidad de sumergirse en la vida cotidiana de la ciudad y experimentarla desde una perspectiva única y personalizada.
             En este trabajo se analizará la oferta de alojamientos de Airbnb en Roma, explorando sus características, tendencias y su impacto en el mercado inmobiliario y turístico de la ciudad.*
             """)
    
    st.markdown("""
                
                El dataset de los anuncios tiene 29357 filas y 75 columnas. En este caso, a partir de ese dataset se ha creado otro con 23 columnas, que serán sobre las que trabajaremos:

                1. ``host:id``: Identificador del anfitrión.
                2. ``host_since``: Fecha en que el anfitrión se unió a Airbnb.
                3. ``host_location``: Ubicación del anfitrión.
                4. ``host_response_rate``: Tasa de respuesta del anfitrión.
                5. ``host_acceptance_rate``: Tasa de aceptación de las solicitudes de reserva por parte del anfitrión.
                6. ``host_is_superhost``: Indicador de si el anfitrión es un superhost o no.
                7. ``host_listings_count``: Número de listados del anfitrión.
                8. ``host_has_profile_pic``: Indicador de si el anfitrión tiene una foto de perfil.
                9. ``neighbourhood_cleansed``: Vecindario de la propiedad después de algún tipo de limpieza o normalización.
                10. ``latitude``: Coordenadas geográficas (latitud) de la propiedad.
                11. ``longitude``: Coordenadas geográficas (longitud) de la propiedad.
                12. ``property_type``: Tipo de propiedad.
                13. ``room_type``: Tipo de habitación ofrecida.
                14. ``accommodates``: Número máximo de personas que pueden ser alojadas en la propiedad.
                15. ``bathrooms_text``: Número de baños en la propiedad.
                16. ``price``: Precio de alquiler por noche de la propiedad.
                17. ``availability_30``: Disponibilidad de la propiedad en los próximos 30 días.
                18. ``availability_60``: Disponibilidad de la propiedad en los próximos 60 días.
                19. ``availability_90``: Disponibilidad de la propiedad en los próximos 90 días.
                20.	``number_of_reviews``: Número total de reseñas.
                21.	``review_scores_rating``: Puntuación global.
                22. ``review_scores_location``: Puntuación de la localización.
                23.	``reviews_per_month``: Promedio de reseñas recibidas por mes para una propiedad en particular.
            
                """  )      
    st.write('------')                    
    st.markdown('### **Visualización del dataframe filtrado:**')
    st.dataframe(df_nopreproc.head())

    

# PÁGINA 2-------------------------------------
elif page == "Preprocesamiento":
    st.write('En primer lugar, tenemos que preprocesar el dataframe. Para ello se han seguido los siguientes pasos:')
    st.markdown("""
                - TRATAMIENTO DE COLUMNAS
                    - Variable ``price``: Quitamos $ y comas
                    - Variables ``host_response_rate`` y ``host_acceptance_rate``: Eliminamos % detrás del número                 
                - TRATAMIENTO DE VALORES NULOS
                    - Imputación con la media: variables con números reales (``host_response_rate``,``host_acceptance_rate``,``price``,``review_scores_rating``,``review_scores_location``,``reviews_per_month``)
                    - Imputación con la mediana: variables con números enteros (``host_listings_count``)                 
                - TRATAMIENTO DE OUTLIERS
                    - Variable ``price``             
                
                
                Para información del código empleado, visita mi GitHub: https://github.com/CrisDAndres/proyecto_airbnb
                
                ---------------------
        """)
    st.markdown('### **Para la visualización de los valores atípicos, obtenemos los parámetros estadísticos de las variables numéricas de interés:**')
    st.code("df.describe().T",language = 'python')
    # Configura la visualización de los números en notación decimal
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    # selecciono las variables que me interesan
    var = df_preproc1[['host_response_rate','host_acceptance_rate','host_is_superhost','host_listings_count','host_has_profile_pic','accommodates','price', 'availability_30', 'availability_60', 'availability_90','number_of_reviews','review_scores_rating','review_scores_location','reviews_per_month']]
    # Aplicar la función describe() solo a las columnas numéricas
    var.describe().T
    st.write('Entre los parámetros estadísticos de las diferentes variables, destaca la desviación estándar de la variable ``price``. Vamos a visualizarla:')
    # Crear el gráfico de cajas y bigotes
    st.set_option('deprecation.showPyplotGlobalUse', False) #Elimino el warning que me sale en el gráfico
    plt.figure(figsize=(10, 5))  # Tamaño del gráfico
    sns.set(style="whitegrid")  # Estilo de la cuadrícula de Seaborn
    fig = sns.boxplot(x="price", data=df_preproc1, color = '#73C4A8')  # Crear el gráfico de cajas y bigotes
    fig.set_xlabel('Precios', fontsize=14)
    # Mostrar el gráfico de seaborn
    st.pyplot()
        
    st.write("""Hay valores atípicos superiores.
                    Consideramos valor atípico superior lo que esté fuera del intervalo ``Q3 + Rango Intercuartílico (IQR) x 1.5``.
                    Reemplazamos esos valores atípicos por ese límite superior.
                    """)
        
    if st.button('Realizar preprocesamiento'):
        with st.spinner('Preprocesando...'):
                # Código de preprocesamiento
                # (No voy a hacerlo en Streamlit, simplemente a visualizarlo)
                #
            st.success('Preprocesamiento completado.')

            st.write('Visualizamos de nuevo el gráfico de cajas de la variable ``price`` y vemos que ya no están esos outliers:')
            plt.figure(figsize=(10, 5))  # Tamaño del gráfico
            sns.set(style="whitegrid")  # Estilo de la cuadrícula de Seaborn
            fig = sns.boxplot(x="price", data=df, color = '#73C4A8')  # Crear el gráfico de cajas y bigotes
            fig.set_xlabel('Precios', fontsize=14)
            # Mostrar el gráfico de seaborn
            st.pyplot()
            st.write('Tampoco hay nulos en las variables de interés, y están las columnas corregidas. El dataframe preprocesado se ve así:')
            st.dataframe(df.head())



# PÁGINA 3-------------------------------------
elif page == "Análisis exploratorio":

    st.markdown("""
                Una vez preprocesados los datos, vamos a explorar las distintas variables para ver la información que nos ofrecen.
                ------------------------                
        """)

    st.markdown('Primero vamos a echar un vistazo al mapa y a los diferentes alojamientos y sus ubicaciones. Si aumentas el mapa, irán apareciendo más:')
    latitudes = df['latitude'].tolist()
    longitudes = df['longitude'].tolist()
    coordenadas = list(zip(latitudes,longitudes))
    # Defino la ubicacion inicial del mapa
    latitud_1 = df['latitude'].iloc[0]
    longitud_1 = df['longitude'].iloc[0]
    # Crear el mapa de Folium con la ubicación inicial especificada
    map = folium.Map(location = [latitud_1,longitud_1],zoom_start=10)
    # Añadir las ubicaciones al mapa generado de Folium
    FastMarkerCluster(data=coordenadas).add_to(map) # Se usa para agrupar los marcadores mas cercanos en clusteres
    folium.Marker(location=[latitud_1,longitud_1]).add_to(map)
    folium_static(map) #con st_folium no me funcionaba en el Explore

    # ---------------------TABS (pestañas)----------------------#
    tab1, tab2, tab3, tab4 = st.tabs(
        ['Análisis de los barrios','Otras variables','Análisis de correlación','Reseñas']) 
    with tab1:
        st.write('En este apartado, podrás obtener diferente información acerca de los alojamientos en los diferentes barrios de Roma, como la cantidad de viviendas de Airbnb, su precio medio o la puntuación media de los alojamientos. Además, podrás explorar de manera interactiva el mapa de Roma. ¡Disfruta explorando!')
        ##  1. Barrio VS Nº alojamientos

        st.markdown('## 1. Barrio VS Nº alojamientos')
        st.write('En primer lugar, nos interesa saber la distribución de los alojamientos por cada barrio. Vemos que en el centro histórico el número de alojamientos o anuncios es mucho mayor en comparación con los demás barrios:')
            
        aloj_barrio = df['neighbourhood_cleansed'].value_counts().sort_values(ascending=True)
            
        #Gráfica de barras de plotly
        fig = px.bar(aloj_barrio, x=aloj_barrio.values, y=aloj_barrio.index,color=aloj_barrio.values, color_continuous_scale='BrBG', text_auto = False) #Con text_auto sale el nombre del conteo en cada barra
        #actualizamos el layout
        fig.update_layout(
                title='Número de alojamientos por barrios de Roma', title_x=0.35, 
                yaxis_title='Barrios de Roma',
                xaxis_title='Número de alojamientos',
                template='plotly_white',
                width=1000, height=500, coloraxis_colorbar_title='Nº alojamientos')  # Agregar título a la leyenda de colores) 

        # Mostrar el gráfico de plotly
        st.plotly_chart(fig)
            
        ## 2. Barrio VS Precio medio

        st.markdown('## 2. Barrio VS Precio medio')
        st.write('También interesaría saber el precio medio por cada barrio. Como era de esperar, alojarse en el centro histórico es más caro:')
            
        barrio_precio = df.groupby('neighbourhood_cleansed')['price'].mean().sort_values(ascending=True)
            
        #Gráfica de barras de plotly
        fig = px.bar(barrio_precio,
                        color=barrio_precio.values,
                        color_continuous_scale='tempo', 
                        template='plotly_white',
                        width=1000, height=500)

        fig.update_layout(title='Precio medio por alojamiento y barrios', title_x=0.35, coloraxis_colorbar_title='Precio medio', 
        xaxis_title='Barrios de Roma',
        yaxis_title='Precio medio por noche')

        # Mostrar el gráfico de plotly
        st.plotly_chart(fig)
         
        ##  3. Barrio VS Puntuación
        st.markdown('## 3. Barrio VS Puntuación')
        st.markdown('También algo importante es saber la puntuación media por cada barrio, en una escala de 0 a 5 ★.')
        st.markdown('**Empezaremos mirando la puntuación general:**')
        # Puntuación general
        punt_barrio_general = df.groupby('neighbourhood_cleansed')['review_scores_rating'].mean().sort_values().reset_index()
        fig = px.bar(punt_barrio_general, x='review_scores_rating', y='neighbourhood_cleansed', color='review_scores_rating', color_continuous_scale='tempo')
        fig.update_layout(height=500, width=1000, title_text="Puntuación de los alojamientos por barrios (0-5 ★)", title_x=0.3,xaxis_title='Puntuación general',yaxis_title='', coloraxis_colorbar_title='Puntuación')  
          # Separar los números del eje y por 1 en 1
        fig.update_yaxes(
        tickvals=list(range(len(punt_barrio_general['neighbourhood_cleansed']))),
        tickmode='array') 
        st.plotly_chart(fig)
            
        st.markdown('**Y ahora la puntuación por la localización:**')
        # Puntuación de la localización
        punt_barrio_localiz = df.groupby('neighbourhood_cleansed')['review_scores_location'].mean().sort_values().reset_index()
        fig = px.bar(punt_barrio_localiz, x='review_scores_location', y='neighbourhood_cleansed', color='review_scores_location', color_continuous_scale='tempo')
        fig.update_layout(height=500, width=1000, title_text="Puntuación de los alojamientos por barrios (0-5 ★)", title_x=0.3,xaxis_title='Puntuación de la localización',yaxis_title='',coloraxis_colorbar_title='Puntuación')
        st.plotly_chart(fig)
        
        # 4. MAPAS INTERACTIVOS
        st.markdown('## 4. MAPAS INTERACTIVOS') 
        st.write('Por último, podemos hacer un análisis de estos 3 puntos visualizándolos mediante mapas interactivos:')
        
        # Abrir archivo html con la información de los mapas generados con folium en modo lectura
        HtmlFile = open("html/rome_map.html", 'r', encoding='utf-8')
        # Leer y cargar en la variable source_code
        source_code = HtmlFile.read() 
        print(source_code)
        # visualizar el contenido en streamlit
        components.html(source_code, height = 600)
        
        st.write('Mediante este mapa de calor podemos ver el precio medio de las viviendas de airbnb:')
        HtmlFile = open("html/rome_hmap.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        print(source_code)
        components.html(source_code, height = 600)
        
    # TAB2----------------------------------

    with tab2:
        st.markdown('## 1. Tipos de alojamiento en los anuncios de Airbnb ')
        st.write("""**Análisis de la cantidad de propiedades diferentes por cada tipo de habitación anunciadas en la plataforma.
                 Se mostrarán las más frecuentes (+ de 200 apariciones) y las menos frecuentes (menos de 50).**""")
    # --------------Alojamientos más frecuentes
        
        # Gráfico de barras plotly de los alojamientos más frecuentes
        aloj = df.groupby(['property_type', 'room_type']).size().reset_index(name='count') # size() calcula el tamaño de cada grupo (nº de room_type de cada grupo de property_type)
        aloj = aloj[aloj['count']>200].sort_values(by=['count']) #Selecciono solo los tipos de propiedad que aparecen más de 200 veces y ordeno los valores por las apariciones        
        colors = {'Entire home/apt': '#F5B041', 'Private room': '#AF7AC5', 'Hotel room': '#16A085','Shared room':'#ABEBC6'}
        fig = px.bar(aloj, y='property_type', x='count', color='room_type',color_discrete_map=colors)  

        fig.update_layout(yaxis={'categoryorder':'total ascending'},
            title='Cantidad de alojamientos más frecuentes (> 200 anuncios)', title_x=0.3, 
            xaxis_title='Cantidad de alojamientos por tipo',
            yaxis_title='Tipo de propiedad',
            template='plotly_white',
            width=1000, height=600, legend_title='Tipo de habitación/apt')
        st.plotly_chart(fig)

        st.write('Se puede observar como el **top3** de alojamientos ofertados más frecuentes son:')
        st.markdown("""           
                  - Vivienda completa
                  - Condominios completos
                  - Habitación privada en vivienda""")
        
        st.markdown('**Ahora voy a graficar los alojamientos menos frecuentes (menos de 50 veces)**')
        aloj = df.groupby(['property_type', 'room_type']).size().reset_index(name='count') 
        aloj = aloj[aloj['count']<5].sort_values(by=['count'],ascending=False) #Selecciono solo los tipos de propiedad que aparecen menos de 50 veces

        fig = px.bar(aloj, y='property_type', x='count', color='room_type',color_discrete_map=colors)

        fig.update_layout(yaxis={'categoryorder':'total ascending'},
            title='Cantidad de alojamientos menos frecuentes (< 50 anuncios)', title_x=0.3, 
            xaxis_title='Cantidad de alojamientos por tipo',
            yaxis_title='Tipo de propiedad',
            template='plotly_white', xaxis=dict(dtick=1),
            width=1000, height=600, legend_title='Tipo de habitación/apt')
        st.plotly_chart(fig)
            
        st.markdown('Se puede observar como los alojamientos ofertados 1 sola vez son algo curiosos, destacando alojamientos en **molinos de viento** *(windmill)*, **castillos** o **barcos**.')
        st.write('-----')
    # --------------Nº de personas que se alojan
        st.markdown('## 2. Nº de personas que se alojan')
        st.write('Se puede observar que lo más frecuente son 2 personas. El máximo es 16, que es lo máximo permitido por Airbnb:')
        
        # Abrir archivo html 
        HtmlFile = open("html/fig1.html", 'r', encoding='utf-8')
        # Leer y cargar en la variable source_code
        source_code = HtmlFile.read() 
        # Código CSS para ajustar la imagen a la pantalla
        css_code = """
        <style>
            img {
                width: 100%;
                height: 100%;
            }
        </style>
        """

        # Combinar el código HTML con el CSS
        html_with_css = f"{css_code}\n{source_code}"
        # visualizar el contenido en streamlit
        components.html(source_code, height = 500, scrolling=True)
        
        st.write('-----')
    # --------------Puntuación general VS Precio

        st.markdown('## 3. Puntuación general VS Precio')
        st.write("""Vamos a observar la relación entre estas 2 variables continuas. Observamos como los alojamientos más caros no son los que tienen una mejor puntuación.
                 Sorprendentemente, la mayor proporción de alojamientos con buenas puntuaciones están por debajo del precio medio:""")
        punt_precio = df.groupby('review_scores_rating')['price'].mean().sort_values().reset_index()
        precio_medio = df['price'].mean().round(2)
        # Crear un scatter plot
        fig = px.scatter(punt_precio, y='price', x='review_scores_rating',opacity=0.7, labels={'price': 'Precio', 'review_scores_rating': 'Puntuación general (0-5)'})
        fig.update_layout(height=500, width=1000, title_text="Relación entre el precio y la puntuación general de los alojamientos", title_x=0.3,xaxis_title="Puntuación general (0-5)", yaxis_title="Precio",
                        )  
        # Actualizar el tamaño de los marcadores
        fig.update_traces(marker=dict(size=7)) 
        # Agregar la línea horizontal para la media del precio
        fig.add_hline(y=precio_medio, line_dash="dot", line_color="red", annotation_text=f"Precio medio: {precio_medio}",
                    annotation_position="top left")
        st.plotly_chart(fig)
        st.write('-----')

    # --------------top10 host

        st.markdown('## 4. Top 10 host')
        st.markdown('Vamos a calcular los 10 host que más anuncios tienen:')
        # Calculamos el top 10 de host con más anuncios
        top10_host=df['host_id'].value_counts().head(10)
        top10_host
        st.markdown('Vemos que el host que más anuncios ha publicado es el número ``23532561``, con **265** anuncios.')
        # Muestro imagen guardada
        image = "img/fig2.png"
        st.image(image, width=700)

        st.markdown('¿Y en total cuál es la proporción de **host/superhost**?')
        # Crear el gráfico de pastel
        colors = ['#16A085', '#922B21']
        fig = px.pie(values=df['host_is_superhost'].value_counts(), names=['No superhost','SUPERHOST'], color_discrete_sequence=colors, hole=0.3)
        fig.update_layout(title='',width=700, height=500, showlegend=True,  title_x=0.5, template = 'plotly_white',legend=dict(
                orientation='h',  # Orientación horizontal
                y=-0.05,  # Desplazamiento vertical desde el gráfico (0-1)
                xanchor='center',  # Ancla en el centro horizontal
                x=0.5  # Desplazamiento horizontal desde el gráfico (0-1)
            ))
        fig.update_traces(textinfo='percent',textfont_size=20, marker = dict(line = dict(color = 'black', width = 0.5)))
        fig.update_traces()

        st.plotly_chart(fig)
        
        st.markdown('De los datos podemos pensar que no es fácil conseguir ser Superhost. **Para conseguir el distintivo, debes ser el propietario del anuncio y tener una cuenta en regla que cumpla los siguientes requisitos:**')

        st.markdown("""
- Haber completado como mínimo 10 estancias o 3 reservas que sumen al menos **100 noches** en total.
- Haber mantenido un índice de respuesta del **90 %** o un porcentaje superior.
- Haber mantenido un índice de cancelación de **menos del 1 %**.
- Haber mantenido una valoración general de **4,8**.""")
    
        #---------------panel powerBI
        st.write('---------')
        st.markdown('#### Podemos ver de manera interactiva la relación entre las variables mediante este panel de Power BI, en el que podrás elegir el barrio que te interese y poder decidir su relación calidad-precio y si se ajusta a tus necesidades:')
        
        # Código HTML del panel de Power BI
        html_code =  """<iframe title="panel_airbnb" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiZjNjMzMwZTUtYzhiMy00NmJlLTg0NGEtMTNlOTI5ODdkODgwIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
        """
        # Insertar el código HTML en la aplicación de Streamlit
        components.html(html_code, height = 1000)
    
    # TAB3----------------------------------
    with tab3:
        st.write('Como no sabemos la distribución de las variables, vamos a utilizar la correlación de ``Spearman``:')

        # Muestro imagen guardada
        image = "img/fig3.png"
        st.image(image, width=1000)
        
        st.write('Algunas de las conclusiones que se pueden observar del gráfico de correlación son las siguientes:')
        st.markdown("""
                    **CORRELACIÓN POSITIVA**
                    - **Ratio aceptación/respuesta**: siguen una correlación moderada positiva (<span style="font-size:20px;">**0.34**</span>).
                    - **Superhost** VS nº reseñas**: tienen una correlación positiva (<span style="font-size:20px;">**0.39**</span>). Además los superhost también tiene una alta correlación con la puntuación general de las reseñas (<span style="font-size:20px;">**0.36**</span>).
                    - **Precio VS nº de alojados**: tienen una fuerte correlación (<span style="font-size:20px;">**0.42**</span>), lo cual indica que a más personas, mayor es el precio de la vivienda.
                    
                    **CORRELACIÓN NEGATIVA**
                    - **Disponibilidad VS Superhost**: tienen una correlación negativa, lo cual indica que hay más probabilidad de que los superhost agoten antes la disponibilidad de sus alojamientos.
                    - **Precio VS reseñas al mes**: tienen correlación negativa (<span style="font-size:20px;">**- 0.16**</span>), lo cual indica que a mayores precios tengan los alojamientos, menos reseñas tienen cada mes.""",unsafe_allow_html=True)

    # TAB4----------------------------------
    with tab4:
        st.markdown('Con las reseñas de los alojamientos, se ha creado una nube de palabras, en la que se pueden ver las palabras más frecuentes en base a su tamaño:')   
      

        wordcloud = "img/nube_airbnb.png"

        st.image(wordcloud,width=400, use_column_width=True)
        st.write('-------')
        st.write('Para información del código empleado, visita mi GitHub: https://github.com/CrisDAndres/proyecto_airbnb')