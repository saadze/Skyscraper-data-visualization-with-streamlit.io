import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
import folium
from functions import *

#### INIT and INPUTS
# importing data
data = pd.read_csv('skyscrapers.csv')

# Streamlit page configuration
st.set_page_config(
    page_title="World's skyscrapers",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)
#list of available countries for the user to choose from
st.sidebar.subheader("Filter by Country:")
selectCountry = st.sidebar.selectbox(
    'Select a country',
    listMaker(data,'Country','All'),
    index=len(listMaker(data,'Country','All'))-1
)
#adding a slider to the side bar for the user to choose a height range
st.sidebar.subheader("Filter by height:")
minSelection, maxSelection = st.sidebar.slider(
    "Height", min_value=0, max_value=830, value=[0, 830]
)
#Group of checkboxes (Skyscrapers' main use)
st.sidebar.subheader("Skyscraper main usage:")
residentialUse = st.sidebar.checkbox("Residential Use",value=True)
commercialUse = st.sidebar.checkbox("Commercial Use",value=True)
others = st.sidebar.checkbox("Others",value=True)
#Choosing specific Skyscrapers
st.sidebar.subheader("Select specific skyscrapers:")
selectTowers = st.sidebar.multiselect(
    'List:',
    listMaker(data,'Name','All')
)


#### MAIN CONTENT
#titles
st.title("World's skyscrapers")
st.subheader('Results:')
#if the user specified specific towers execute this
if len(selectTowers) > 0:
    #getting the sorted data and initializing the map 
    finalInfos= sortData(specificTowers(data,selectTowers),country=selectCountry,height={'min':minSelection,'max':maxSelection},types={'r':residentialUse,'c':commercialUse,'o':others})
    finalMap = folium.Map(location=[0.0,0.0], zoom_start=1, tiles="Stamen Terrain")
    tooltip= "Infos >"
    #for each tower, rendering elements on map
    for i,row in finalInfos.iterrows():
        #creating a pop uo Iframe(html) message
        message= f"{row['name']}\nHeight: {row['height']} m \n Fun Fact: {row['remark']}"
        html = f'''Name: {row['name']}<br>
        Height: {row['height']} m<br>
        Fun Fact: {row['remark']}'''
        iframe = folium.IFrame(html,
                        width=150,
                        height=150)

        message = folium.Popup(iframe,
                            max_width=150)
        #adding a marker to the map
        folium.Marker(
            [row['lat'], row['lon']],
            popup=message,
            tooltip=tooltip,
            icon=folium.Icon(color=row['colors'])
        ).add_to(finalMap)
    #displaying the map
    folium_static(finalMap)
else:
    #getting the sorted data and initializing the map 
    finalInfos= sortData(data,country=selectCountry,height={'min':minSelection,'max':maxSelection},types={'r':residentialUse,'c':commercialUse,'o':others})
    finalMap = folium.Map(location=[0.0,0.0], zoom_start=1, tiles="Stamen Terrain")
    tooltip= "Infos >"
    #for each tower, rendering elements on map
    for i,row in finalInfos.iterrows():
        #creating a pop uo Iframe(html) message
        message= f"{row['name']}\nHeight: {row['height']} m \n Fun Fact: {row['remark']}"
        html = f'''Name: {row['name']}<br>
        Height: {row['height']} m<br>
        Fun Fact: {row['remark']}'''
        iframe = folium.IFrame(html,
                        width=150,
                        height=150)

        message = folium.Popup(iframe,
                            max_width=150)
        #adding a marker to the map
        folium.Marker(
            [row['lat'], row['lon']],
            popup=message,
            tooltip=tooltip,
            icon=folium.Icon(color=row['colors'])
        ).add_to(finalMap)
    #displaying the map
    folium_static(finalMap)
st.subheader('Explore Raw data')
st.write(data)