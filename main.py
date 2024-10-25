import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
import io

# Function to create KML content with FormId as title, Object as description, and latitude before longitude
def create_kml(df):
    kml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
    """
    for _, row in df.iterrows():
        form_id = row['FormId']
        obj = row['Object']
        lat = row['Latitude']
        lon = row['Longitude']
        kml_content += f"""
        <Placemark>
          <name>{form_id}</name>
          <description>{obj}</description>
          <Point>
            <coordinates>{lat},{lon},0</coordinates>
          </Point>
        </Placemark>
        """
    kml_content += """
      </Document>
    </kml>
    """
    return kml_content

# Function to generate a demo CSV file
def generate_demo_csv():
    demo_data = {
        'FormId': ['F001', 'F002'],
        'Object': ['Plant1', 'Plant2'],
        'Latitude': [22.666838096303614, 22.667000096303614],
        'Longitude': [77.64103521144537, 77.64110021144537]
    }
    demo_df = pd.DataFrame(demo_data)
    return demo_df.to_csv(index=False).encode('utf-8')

# Streamlit layout
st.title("KML Generator and Map Visualizer from Plant Data")
st.write("Upload your CSV file, generate a KML file, visualize the coordinates on a map, and download the KML.")

# Download demo CSV file button
st.download_button(
    label="Download Demo CSV",
    data=generate_demo_csv(),
    file_name="demo_plant_count.csv",
    mime="text/csv"
)

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file:
    # Load data without height column
    df = pd.read_csv(uploaded_file)
    df = df[['FormId', 'Object', 'Latitude', 'Longitude']]
    st.write("Uploaded CSV Data:", df)
    
    # Generate KML content
    kml_content = create_kml(df)
    
    # KML file download
    kml_bytes = kml_content.encode("utf-8")
    st.download_button(
        label="Download KML File",
        data=kml_bytes,
        file_name="plant_count.kml",
        mime="application/vnd.google-earth.kml+xml"
    )
    
    # Folium map visualization
    map_center = [df['Latitude'].mean(), df['Longitude'].mean()]
    m = folium.Map(location=map_center, zoom_start=13)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"{row['FormId']}: {row['Object']}",
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)

    # Display map in Streamlit
    st.write("Map Visualization:")
    folium_static(m, width=700, height=500)
