import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd

df = pd.read_csv('folium_data.csv')

chems = list(df.columns)
chems = chems[3:]

AX_df = pd.read_csv('AX_folium.csv')
WCX_df = pd.read_csv('WCX_folium.csv')

# Define the function to create the map for each chemical
def create_map(chem, df):
    m_glyph = folium.Map(location=[df['Lat'].mean(), df['Long'].mean()], zoom_start=10)
    for index, value in df[chem].items():
        row = df.loc[index]
        if value > 0:
            folium.CircleMarker(
                location=[row['Lat'], row['Long']],
                radius=value,
                color='#FF3D1F',
                fill=True,
                fill_color='#FF3D1F',
                fill_opacity=0.5
            ).add_to(m_glyph)
        else:
            folium.Marker(
                location=[row['Lat'], row['Long']],
                icon=folium.DivIcon(html='<i class="fa fa-times fa-2x" style="color:black;"></i>')
            ).add_to(m_glyph)
    return m_glyph

# Define the app pages
pages = {
    chem: create_map(chem, AX_df) for chem in chems
}

# Add the WCX maps to the pages
for chem in chems:
    pages[chem + ' (WCX)'] = create_map(chem, WCX_df)

# Define the Streamlit app
def app():
    st.set_page_config(page_title='Chemical Maps')

    st.title('Chemical Maps')

    # Create a sidebar with links to each chemical page
    st.sidebar.title('Chemicals')
    selected_chem = st.sidebar.radio('', chems)

    # Display the selected chemical's map
    st.markdown(f"## {selected_chem}")
    st.markdown("### AX")
    folium_static(pages[selected_chem])
    st.markdown("### WCX")
    folium_static(pages[selected_chem + ' (WCX)'])

if __name__ == '__main__':
    app()