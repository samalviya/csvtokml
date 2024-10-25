import pandas as pd
import streamlit as st
import io

# Function to create KML content
def create_kml(df):
    kml_content = """<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
    """
    for _, row in df.iterrows():
        obj = row['Object']
        lon = row['Longitude']
        lat = row['Latitude']
        hight = row['PLANT_HEIGHT(IN FEET)']
        kml_content += f"""
        <Placemark>
          <name>{obj}</name>
          <description>{hight}</description>
          <Point>
            <coordinates>{lon},{lat},0</coordinates>
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
        'Object': ['Plant1', 'Plant2'],
        'Longitude': [77.64103521144537, 77.64110021144537],
        'Latitude': [22.666838096303614, 22.667000096303614],
        'PLANT_HEIGHT(IN FEET)': [5, 6]
    }
    demo_df = pd.DataFrame(demo_data)
    return demo_df.to_csv(index=False).encode('utf-8')

# Streamlit layout
st.title("KML File Generator from Plant Count Data")
st.write("Upload your CSV file, generate a KML file, and visualize your data.")

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
    # Load data
    df = pd.read_csv(uploaded_file)
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
    
    # Display KML preview and visualization
    st.write("Generated KML Content Preview:")
    st.text(kml_content[:500])  # Show first 500 characters

    # Here you could add map visualization if you have coordinate data
