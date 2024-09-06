import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from pyeuropeana import apis
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Ensure that the API key is set
if 'EUROPEANA_API_KEY' not in os.environ:
    st.error("EUROPEANA_API_KEY is not set in the environment variables. Please set it and restart the app.")
    st.stop()

def get_provider_data(provider_name, rows=1000):
    myquery = apis.search(
        query='pl_wgs84_pos_lat:(*)',
        qf=f'DATA_PROVIDER:"{provider_name}"',
        rows=rows
    )
    
    myquery_df = pd.DataFrame(myquery["items"], columns=['edmPlaceLatitude', 'edmPlaceLongitude', 'id', 'country', 'dataProvider', 'dcCreator'])
    
    def extract_single(x):
        return x[0] if isinstance(x, list) and len(x) > 0 else x
    
    for col in ['edmPlaceLatitude', 'edmPlaceLongitude', 'country', 'dataProvider', 'dcCreator']:
        myquery_df[col] = myquery_df[col].apply(extract_single)
    
    myquery_df['edmPlaceLatitude'] = pd.to_numeric(myquery_df['edmPlaceLatitude'], errors='coerce')
    myquery_df['edmPlaceLongitude'] = pd.to_numeric(myquery_df['edmPlaceLongitude'], errors='coerce')
    
    return myquery_df

# Set up the Streamlit app
st.title('Europeana Data Explorer')

# Input for provider name
provider_name = st.text_input('Enter the name of the data provider:')

# Button to trigger data fetch
if st.button('Fetch Data'):
    if provider_name:
        # Show loading message
        with st.spinner('Fetching data...'):
            # Get the data
            df = get_provider_data(provider_name)
        
        # Display the data
        st.subheader(f'Data from {provider_name}')
        st.write(f'Number of items retrieved: {len(df)}')
        
        # Display the first few rows
        st.subheader('First few rows of data:')
        st.write(df.head())
        
        # Create a map centered on the mean latitude and longitude
        valid_coords = df.dropna(subset=['edmPlaceLatitude', 'edmPlaceLongitude'])
        if not valid_coords.empty:
            center_lat = valid_coords['edmPlaceLatitude'].mean()
            center_lon = valid_coords['edmPlaceLongitude'].mean()
            m = folium.Map(location=[center_lat, center_lon], zoom_start=2)

            # Add markers for each item
            for _, row in valid_coords.iterrows():
                folium.Marker(
                    location=[row['edmPlaceLatitude'], row['edmPlaceLongitude']],
                    popup=f"ID: {row['id']}<br>Creator: {row['dcCreator']}<br>Country: {row['country']}",
                    tooltip=row['id']
                ).add_to(m)

            # Display the map
            st.subheader('Map of Object Locations')
            folium_static(m)
        else:
            st.warning('No valid coordinates found in the data.')
        
        # Option to download the full dataset
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download full dataset as CSV",
            data=csv,
            file_name=f"{provider_name}_data.csv",
            mime="text/csv",
        )
    else:
        st.warning('Please enter a provider name.')

# Run this app with: streamlit run app.py