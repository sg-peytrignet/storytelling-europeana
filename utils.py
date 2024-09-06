import pandas as pd
from pyeuropeana import apis
import geopandas as gpd

def get_provider_data(provider_name, world_gdf, rows=1000):
    """
    Query Europeana API for a specific data provider and return processed DataFrames.
    
    Args:
    provider_name (str): Name of the data provider to query
    world_gdf (GeoDataFrame): World map GeoDataFrame for spatial join
    rows (int): Number of rows to retrieve (default 1000)
    
    Returns:
    tuple: (pandas.DataFrame, geopandas.GeoDataFrame)
        - First DataFrame: Processed DataFrame with the queried data, including object location
        - Second GeoDataFrame: Count of objects per country from the world dataset, including geometry
    """
    # Query the Europeana API
    myquery = apis.search(
        query='pl_wgs84_pos_lat:(*)',
        qf=f'DATA_PROVIDER:"{provider_name}"',
        rows=rows
    )
    
    # Create initial DataFrame
    myquery_df = pd.DataFrame(myquery["items"], columns=['edmPlaceLatitude', 'edmPlaceLongitude', 'id', 'country', 'dataProvider', 'dcCreator'])
    
    # Function to extract single value from list or return original value
    def extract_single(x):
        return x[0] if isinstance(x, list) and len(x) > 0 else x
    
    # Apply extraction to relevant columns
    for col in ['edmPlaceLatitude', 'edmPlaceLongitude', 'country', 'dataProvider', 'dcCreator']:
        myquery_df[col] = myquery_df[col].apply(extract_single)
    
    # Convert latitude and longitude to float type
    myquery_df['edmPlaceLatitude'] = pd.to_numeric(myquery_df['edmPlaceLatitude'], errors='coerce')
    myquery_df['edmPlaceLongitude'] = pd.to_numeric(myquery_df['edmPlaceLongitude'], errors='coerce')
    
    # Create a GeoDataFrame from the DataFrame
    gdf = gpd.GeoDataFrame(
        myquery_df, 
        geometry=gpd.points_from_xy(myquery_df.edmPlaceLongitude, myquery_df.edmPlaceLatitude), 
        crs="EPSG:4326"
    )

    # Perform spatial join
    gdf_with_country = gpd.sjoin(gdf, world_gdf[['geometry', 'name']], how='left', op='within')

    # Add the new column to the original DataFrame
    myquery_df['object_location'] = gdf_with_country['name']

    # Fill NaN values (points that don't fall within any country) with "Unknown"
    myquery_df['object_location'] = myquery_df['object_location'].fillna("Unknown")
    
    # Create world_counts directly from the spatial join result
    world_counts = world_gdf.copy()
    country_counts = gdf_with_country['name'].value_counts()
    world_counts['object_count'] = world_counts['name'].map(country_counts).fillna(0).astype(int)
    
    return myquery_df, world_counts

def aggregate_location_counts(df):
    """
    Aggregate the data by object_location and get counts.
    
    Args:
    df (pandas.DataFrame): DataFrame containing 'object_location' column
    
    Returns:
    pandas.DataFrame: DataFrame with object locations and their counts, sorted by count
    """
    location_counts = df['object_location'].value_counts().reset_index()
    location_counts.columns = ['object_location', 'count']
    return location_counts.sort_values('count', ascending=False)