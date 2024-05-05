# ---------------------LIBRARIES----------------------#
import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import numpy as np
import pandas as pd
import warnings
import base64
from pandas.errors import SettingWithCopyWarning
# Graphics
import seaborn as sns
import matplotlib.pyplot as plt
import plotly_express as px
from plotly.subplots import make_subplots
# interactive maps
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import folium_static
# prediction
import xgboost as xgb
import json
from joblib import load
from pycaret.regression import load_model


warnings.simplefilter(action='ignore', category=(SettingWithCopyWarning))
 

# ---------------------SITE CONFIG----------------------#
st.set_page_config(
    page_title="Airbnb: Roma",
    page_icon="🏛️",
    layout="centered", 
    initial_sidebar_state="collapsed", 
)

# # ---------------------MENU----------------------# 

#header image
st.image("img/mask.png")

page = option_menu(None, ["Home", "Neighbourhoods", "Other information", "Power BI dashboard", "Reviews", "Price predictor"], 
    icons=["house", "pin-map", "plus", "clipboard-plus", "table", "coin"], 
    default_index=0, orientation="horizontal",
    styles={
        "nav-link": {"font-size": "14px", "text-align": "center", "margin": "0px", "padding": "0px", "--hover-color": "#eee"},
        "icon": {"margin": "auto", "display": "block"}  # Centered icons
    }
)

# ---------------------LOAD DATA----------------------#

# read data
@st.cache_data()
def load_data():
    df = pd.read_csv("data/airbnb_limpio.csv")
    return df

# load data
df = load_data()

# ---------------------BACKGROUND IMAGE----------------------#

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
     <style>
        .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local("img/rome_background.png")  

# ---------------------BODY----------------------#

# PAGE 1-------------------------------------
if page == "Home":
    
    st.markdown("""
                ***Rome, the Eternal City, has been a crossroads of cultures and religions for more than two millennia.
                Located in the Lazio region, Rome is the capital of Italy and the largest city on the Italian peninsula.
                Today it is a vibrant metropolis that combines the grandeur of its past with the vitality of a modern city, attracting millions of tourists every year.***
                """)

    st.markdown("""
             *In this context, the Airbnb accommodation market in Rome plays an important role, offering visitors the opportunity to immerse themselves in the daily life of the city and experience it from a unique and personal perspective.
             This app analyses the supply of Airbnb accommodation in Rome, exploring its characteristics, trends and impact on the city's real estate and tourism markets.*
             """)
    
    st.markdown("""
                
                The Advertisements dataset has 29357 rows and 75 columns. In this case, we have created another record with 23 columns, which we are going to work on:

                1. ``host:id``:  Host identifier.
                2. ``host_since``: Date the host joined Airbnb.
                3. ``host_location``: Location of the host.
                4. ``host_response_rate``: Response rate of the host.
                5. ``host_acceptance_rate``: Host acceptance rate of booking requests.
                6. ``host_is_superhost``: Indicates whether the host is a superhost or not.
                7. ``host_listings_count``: Number of listings for the host.
                8. ``host_has_profile_pic``: Indicates if the host has a profile picture.
                9. ``neighbourhood_cleansed``: Neighbourhood of the property after some cleaning or normalisation.
                10. ``latitude``: Geographical coordinates (latitude) of the property.
                11. ``longitude``: Geographical coordinates (longitude) of the property.
                12. ``property_type``: Type of property.
                13. ``room_type``: Type of room offered.
                14. ``accommodates``: Maximum number of persons that can be accommodated in the property.
                15. ``bathrooms_text``: Number of bathrooms in the property.
                16. ``price``: Price per night from
                17. ``availability_30``: Availability of the property in the next 30 days.
                18. ``availability_60``: Availability of the property in the next 60 days.
                19. ``availability_90``: Availability of the property in the next 90 days.
                20.	``number_of_reviews``: Total number of reviews.
                21.	``review_scores_rating``: Overall rating.
                22. ``review_scores_location``: Location score.
                23.	``reviews_per_month``: Average number of reviews received per month for a given property.
            
                """  )      
    st.write('------')                    
    st.markdown('### **Visualisation of the pre-processed dataframe:**')
    st.dataframe(df.head())
    st.write('Information about the code used can be found on my GitHub: https://github.com/CrisDAndres/proyecto_airbnb')

# PAGE 2-------------------------------------
elif page == "Neighbourhoods":

    st.markdown('Here you can see the different accommodations on offer and where they are located. Zoom in on the map to see more:')
    latitud = df['latitude'].tolist()
    longitud = df['longitude'].tolist()
    coordinates = list(zip(latitud,longitud))
    # define the initial location of the map
    latitud_1 = df['latitude'].iloc[0]
    longitud_1 = df['longitude'].iloc[0]
    # create the Folium map with the specified starting location
    map = folium.Map(location = [latitud_1,longitud_1],zoom_start=10)
    # Adding locations to the generated Folium map
    FastMarkerCluster(data=coordinates).add_to(map) # It is used to group the closest markers into clusters.
    folium.Marker(location=[latitud_1,longitud_1]).add_to(map)
    folium_static(map) 
    
    st.markdown("""
            ### What would you like to know? Select a tab:              
        """)

    # ---------------------TABS (pestañas)----------------------#
    tab1, tab2, tab3, tab4 = st.tabs(
        ['Accomodations','Price', 'Score','Maps']) 
    with tab1:
        
        ##  1. Neighbourhood VS No. of accommodations

        st.markdown('### Neighbourhood VS No. of accommodations')
        st.write('First of all, we are interested in the distribution of accommodation in each neighbourhood. We can see that in the historic centre the number of accommodations or advertisements is much higher than in the other districts:')
            
        accom_neigh = df['neighbourhood_cleansed'].value_counts().sort_values(ascending=True)
            
        #Plotly bar chart
        fig = px.bar(accom_neigh, x=accom_neigh.values, y=accom_neigh.index,color=accom_neigh.values, color_continuous_scale='BrBG', text_auto = False) 
        fig.update_layout(
                title='Number of accommodations by neighbourhood in Rome', title_x=0.23, 
                yaxis_title='Neighbourhoods',
                xaxis_title='No. of Airbnb offers',
                template='plotly_white',
                width=690, height=500, coloraxis_colorbar_title='No. of Airbnb offers')   

        st.plotly_chart(fig)
   
    with tab2:
                
        ## 2. Neighbourhood VS Average price

        st.markdown('### Neighbourhood VS Average price')
        st.write('It would also be interesting to know the average price for each neighbourhood. As expected, staying in the historic centre is more expensive:')
            
        neigh_price = df.groupby('neighbourhood_cleansed')['price'].mean().sort_values(ascending=True)
            
        #Plotly bar chart
        fig = px.bar(neigh_price,
                        color=neigh_price.values,
                        color_continuous_scale='tempo', 
                        template='plotly_white',
                        width=690, height=500)

        fig.update_layout(title='Average price per accommodation and neighbourhood', title_x=0.23, coloraxis_colorbar_title='Average price', 
        xaxis_title='Neighbourhoods',
        yaxis_title='Average price per night')

        st.plotly_chart(fig)
    
    with tab3:
                 
        ##  3. Neighbourhood VS Score
        st.markdown('### Neighbourhood VS Score')
        st.markdown('It is also important to know the average score for each neighbourhood, on a scale of 0 to 5 ★.')
        
        st.markdown('**We will start by looking at the overall score:**')
        # General score
        general_score_neigh = df.groupby('neighbourhood_cleansed')['review_scores_rating'].mean().sort_values().reset_index()
        fig = px.bar(general_score_neigh, x='review_scores_rating', y='neighbourhood_cleansed', color='review_scores_rating', color_continuous_scale='tempo')
        fig.update_layout(height=500, width=690, title_text="Accommodation score by neighbourhood (0-5 ★)", title_x=0.23,xaxis_title='General score',yaxis_title='', coloraxis_colorbar_title='Score')  
        
        fig.update_yaxes(
        tickvals=list(range(len(general_score_neigh['neighbourhood_cleansed']))),
        tickmode='array') 
        st.plotly_chart(fig)
            
        st.markdown('**And now the localisation score:**')
        # Localisation score
        loc_score_neigh = df.groupby('neighbourhood_cleansed')['review_scores_location'].mean().sort_values().reset_index()
        fig = px.bar(loc_score_neigh, x='review_scores_location', y='neighbourhood_cleansed', color='review_scores_location', color_continuous_scale='tempo')
        fig.update_layout(height=500, width=690, title_text="Accommodation score by neighbourhood (0-5 ★)", title_x=0.23,xaxis_title='Localisation score',yaxis_title='',coloraxis_colorbar_title='Score')
        st.plotly_chart(fig)
    
    with tab4:
            
        # 4. INTERACTIVE MAPS
        st.markdown('### INTERACTIVE MAPS') 
        st.write('Finally, we can analyse these 3 points by visualising them on interactive maps. There are two different layers, so you can decide whether you want to see the neighbourhoods by average price or by overall score:')
        
        # Open html file with the information of the maps generated with folium in read mode.
        HtmlFile = open("html/rome_map.html", 'r', encoding='utf-8')
        # Read and load into source_code variable
        source_code = HtmlFile.read() 
        print(source_code)
        # view content on streamlit
        components.html(source_code, height = 600)
        
        
# PAGE 3----------------------------------
elif page == "Other information":
    
    # --------------Most common accommodation
        
        st.markdown('### 1. Types of accommodation in Airbnb listings')
        st.write("""**Analysis of the number of properties for each type of space advertised on the platform.
                 The most frequent (+ 200 appearances) and the least frequent (less than 50) are displayed.**""")
        
        # Bar chart plotly of the most frequent accommodations
        accom = df.groupby(['property_type', 'room_type']).size().reset_index(name='count') # size() calculates the size of each group (no. of room_type of each property_type group)
        accom1 = accom[accom['count']>200].sort_values(by=['count']) 
        accom2 = accom[accom['count']<5].sort_values(by=['count'],ascending=False) 
        
        # define colors
        colors = {'Entire home/apt': '#F5B041', 'Private room': '#AF7AC5', 'Hotel room': '#16A085','Shared room':'#ABEBC6'}
        # Make subplots
        fig = make_subplots(rows=1, cols=2)

        fig = px.bar(accom1, y='property_type', x='count', color='room_type',color_discrete_map=colors)  

        fig.update_layout(yaxis={'categoryorder':'total ascending'},
            title='Number of most frequent accommodations (> 200 listings)', title_x=0.2, 
            xaxis_title='Number of accommodations by type',
            yaxis_title='Property type',
            template='plotly_white',
            width=690, height=600, legend_title='Room/apt type')
        st.plotly_chart(fig)

        st.write('-----')
    
        fig = px.bar(accom2, y='property_type', x='count', color='room_type',color_discrete_map=colors)

        fig.update_layout(yaxis={'categoryorder':'total ascending'},
            title='Number of less frequent accommodations (< 50 listings)', title_x=0.23, 
            xaxis_title='Number of accommodations by type',
            yaxis_title='Property type',
            template='plotly_white', xaxis=dict(dtick=1),
            width=695, height=600, legend_title='Room/apt type')
        st.plotly_chart(fig)
            
        st.write('-----')
    
    # --------------No. of people staying
        st.markdown('### 2. No. of people staying')
        st.write('You can see that the most common number is 2 people. The maximum is 16, which is the maximum allowed by Airbnb:')
        
        Accomm = df['accommodates'].value_counts().sort_index()

        fig = px.bar(Accomm, x=Accomm.index, y=Accomm.values, color_discrete_sequence=['#16A085'])
        fig.update_layout(
            title='Number of persons staying in accommodations', title_x=0.25, 
            yaxis_title='No. of accommodations',
            xaxis_title='No. of people',
            template='plotly_white',
            width=695, height=500) 
        fig.update_xaxes(dtick=1)     
        st.plotly_chart(fig)
        st.write('-----')
    
    
    # --------------General score VS Price

        st.markdown('### 3. General score VS Price')
        st.write("""Let's look at the relationship between these 2 continuous variables. We see that the most expensive accommodations are not the ones with the best scores.
                 Surprisingly, the highest proportion of accommodations with good scores are below the average price:""")
        score_price = df.groupby('review_scores_rating')['price'].mean().sort_values().reset_index()
        mean_price = df['price'].mean().round(2)
        # scatter plot
        fig = px.scatter(score_price, y='price', x='review_scores_rating',opacity=0.7, labels={'price': 'Price', 'review_scores_rating': 'General score (0-5)'})
        fig.update_layout(height=500, width=695, title_text="Relationship between price and general accommodation score", title_x=0.2,xaxis_title="General score (0-5)", yaxis_title="Price",
                  )  
        fig.update_traces(marker=dict(size=7)) 
        # Add the horizontal line for the average of the price
        fig.add_hline(y=mean_price, line_dash="dot", line_color="red", annotation_text=f"Mean price: {mean_price}",
                    annotation_position="top left")
        st.plotly_chart(fig)
        st.write('-----')

    # --------------top10 host

        st.markdown('## 4. Top10 host')
        st.markdown("Let's calculate the top 10 hosts with the highest number of listings:")
        # Calculate the top10 host with the most listings
        top10_host=df['host_id'].value_counts().head(10)
        # Filter the original DataFrame to include only the rows of the top 10 hosts
        df_top10_host = df[df['host_id'].isin(top10_host.index)]
        df_top10_host['host_listings_count'].sort_values()
        
        st.set_option('deprecation.showPyplotGlobalUse', False) #remove the warning that I get in the graphic.

        plt.figure(figsize=(8, 5))
        sns.set_style("white") 
        colors = {"f": '#16A085', "t": '#922B21'}

        fig = sns.countplot(data=df_top10_host, y='host_id',hue='host_is_superhost',palette=colors)

        fig.set_xlabel('Number of listings published', fontsize=10) 
        fig.set_ylabel('Host ID', fontsize=10) 

        fig.tick_params(axis='y', labelsize=10)
        fig.tick_params(axis='x', labelsize=10)
        plt.legend(title='¿Superhost?', labels=['Yes', 'No'], fontsize=10)
        st.pyplot()
        
        st.markdown('We see that the host with the most ads is the number ``23532561``, with **265** ads. This is probably a company that is professionally involved in holiday rentals.')
        st.markdown('Of those 10, only 2 are **superhost**.')
    
        st.markdown('And in total what is the **host/superhost** ratio?')
        # Pie chart
        colors = ['#16A085', '#922B21']
        fig = px.pie(values=df['host_is_superhost'].value_counts(), names=['No superhost','SUPERHOST'], color_discrete_sequence=colors, hole=0.3)
        fig.update_layout(title='',width=700, height=500, showlegend=True,  title_x=0.5, template = 'plotly_white',legend=dict(
                orientation='h',  # Horizontal orientation
                y=-0.05,  # Vertical offset from the graph (0-1)
                xanchor='center',  
                x=0.5  # Horizontal offset from the graph (0-1)
            ))
        fig.update_traces(textinfo='percent',textfont_size=20, marker = dict(line = dict(color = 'black', width = 0.5)))
        fig.update_traces()

        st.plotly_chart(fig)
        
        st.markdown('From the data we can see that it is not easy to become a Superhost. **To get the badge, you must be the owner of the ad and have an account in good standing that meets the following requirements:**')

        st.markdown("""
- Completed at least 10 stays or 3 bookings totalling at least **100 nights**.
- Maintained a response rate of **90%** or higher.
- Maintained a cancellation rate of **less than 1%**.
- Maintained an overall rating of **4.8**.""")
        
        # --------------correlation
        
        st.write('As we do not know the distribution of the variables, we will use the Spearman correlation:')
        #replace categorical variables with numbers.
        dict_profilepic = {'f':0,'t':1}
        dict_superhost = {'f':0,'t':1}
        df['host_has_profile_pic'] = df['host_has_profile_pic'].replace(dict_profilepic)
        df['host_is_superhost'] = df['host_is_superhost'].replace(dict_superhost)
        
        # Spearman's method (measures non-parametric and monotonic dependence between variables).
        var = df[['host_response_rate','host_acceptance_rate','host_is_superhost','host_listings_count','host_has_profile_pic','accommodates','price', 'availability_30', 'availability_60', 'availability_90','number_of_reviews','review_scores_rating','review_scores_location','reviews_per_month']]
        corr = var.corr(method='spearman',numeric_only=True) 
        # Generate a mask for the upper triangle
        mask = np.triu(np.ones_like(corr, dtype=bool)) 
        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(15,13))       
        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(145, 300, s=60, as_cmap=True)
        # Draw the heatmap with the mask and correct aspect ratio
        sns.heatmap(corr, mask=mask[0:30,0:30], cmap=cmap, vmax=1, center=0, vmin=-1,  
                    square=True, linewidths=1, cbar_kws={"shrink": 1}, annot = True)      # cbar_kws={"shrink": 1} es el tamaño de la barra de color
        st.pyplot()
        
        st.write('Some of the conclusions that can be drawn from the correlation graph are as follows:')
        st.markdown("""
                    **POSITIVE CORRELATION**
                    - **Acceptance/response ratio**: follow a moderate positive correlation (<span style="font-size:20px;">**0.34**</span>).
                    - **Superhost** VS **No. of reviews**: follow a positive correlation (<span style="font-size:20px;">**0.39**</span>). In addition, superhost also has a high correlation with the general review score (<span style="font-size:20px;">**0.36**</span>).
                    - **Price VS No. of housed persons**: have a strong correlation (<span style="font-size:20px;">**0.42**</span>), indicating that the more people, the higher the house price.
                    
                    **NEGATIVE CORRELATION**
                    - **Availability VS Superhost**: have a negative correlation, suggesting that superhosts are more likely to use up their availability earlier.
                    - **Price VS reviews per month**: have a negative correlation (<span style="font-size:20px;">**- 0.16**</span>), indicating that the higher the prices of accommodation, the fewer reviews they have each month.""",unsafe_allow_html=True)

# PAGE 4-------------------------------------
elif page == "Power BI dashboard":
        st.write('---------')
        st.markdown(
            '<div style="text-align: justify;">'
            'We can interactively see the relationship between the variables using this Power BI dashboard, where you can select the neighbourhood you are interested in and decide its value for money and whether it fits your needs:'
            '</div>',
            unsafe_allow_html=True
        )            
        # HTML code of the Power BI dashboard
        html_code = """
        <div style="display: flex; justify-content: center;">
            <iframe title="panel_airbnb" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiZjNjMzMwZTUtYzhiMy00NmJlLTg0NGEtMTNlOTI5ODdkODgwIiwidCI6IjhhZWJkZGI2LTM0MTgtNDNhMS1hMjU1LWI5NjQxODZlY2M2NCIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>
        </div>
        """

        st.markdown(html_code, unsafe_allow_html=True)

# PAGE 5-------------------------------------
elif page == "Reviews":
        st.markdown('A word cloud has been created from the accommodation reviews to show you the most common words based on their size:')   
      

        wordcloud = "img/nube_airbnb.png"

        st.image(wordcloud,width=500, use_column_width=True)

# PAGE 6-------------------------------------
elif page == "Price predictor":
    st.markdown("""
        <div style='text-align: center;'>
            <h1>Price prediction for Airbnb accommodation in Rome</h1>
        </div>
    """, unsafe_allow_html=True)
    
    ## -- File upload 
    scaler = load('outputs/scaler.pkl')
    model = load_model('models/price_xbg') #load the model trained with xbg
    # Open JSON file in read mode
    with open("outputs/mapeo.json", "r") as json_fie:
        # Loads the content of the JSON file into a dictionary
        encoder = json.load(json_fie)
        
    with open("outputs/mapeo_inverso.json", "r") as json_fie:    
        decoder = json.load(json_fie)


    municipi_options = [
    'I Centro Storico',
    'II Parioli/Nomentano',
    'III Monte Sacro',
    'IV Tiburtina',
    'V Prenestino/Centocelle',
    'VI Roma delle Torri',
    'VII San Giovanni/Cinecittà',
    'VIII Appia Antica',
    'IX Eur',
    'X Ostia/Acilia',
    'XI Arvalia/Portuense'
    'XII Monte Verde',
    'XIII Aurelia',
    'XIV Monte Mario'
    'XV Cassia/Flaminia',
    ]

    # --------------------------------------------------------------------------------------

    with st.form("prediction_form"): 
        beds = st.number_input('No. of beds:', value=1)
        accom = st.number_input('No. of travellers:', value=1)
        bath = st.number_input('No. of bathrooms:', value=1)
        barrio = st.selectbox('Choose the district of Rome you are interested in:', municipi_options)
        submit_button = st.form_submit_button(label='Predict the price')

    if submit_button:
        input_data = pd.DataFrame([[beds, accom, bath, barrio]],
                                columns=['beds', 'accommodates', 'bathrooms', 'neighbourhood_cleansed']) 

    # 1- Encode what the user types into numbers using the mapping json.
        input_data['neighbourhood_cleansed'] = input_data['neighbourhood_cleansed'].replace(encoder)
        
    # 2 - Normalise the input data
        input_data_scaled = scaler.transform(input_data)
        dtest = xgb.DMatrix(input_data_scaled) # convert the input data into a DMatrix object, the format used by XGBoost to make predictions.

    # 3 - Make the prediction with the trained model
        prediction = model.predict(dtest)
        
        predicted_price = prediction[-1]  # Generally, the prediction is in the last column.
        st.write(f"### The predicted price of the accommodation is {predicted_price:.2f} €")

