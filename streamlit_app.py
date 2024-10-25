import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

dataset = pd.read_csv('https://raw.githubusercontent.com/JuliethSuarezPoveda/gdp-dashboard/refs/heads/main/fincaraiz_final.csv')

dataset['title'] = dataset['title'].str.replace('en arriendo', '', regex=False)
dataset['title'] = dataset['title'].str.replace('en Arriendo', '', regex=False)
dataset['title'] = dataset['title'].str.replace('Arriendo', '', regex=False)
dataset['title'] = dataset['title'].str.replace('en', '', regex=False)
dataset['title'] = dataset['title'].str.replace(', Bogotá', '', regex=False)
dataset['title'] = dataset['title'].str.replace('en Arriendo ', '', regex=False)
dataset['title'] = dataset['title'].str.replace('en Arriendo  ', '', regex=False)
dataset['title'] = dataset['title'].str.replace(', Bogotá - Santa Bárbara', '', regex=False)
dataset['title'] = dataset['title'].str.replace('- Chicó Norte', '', regex=False)
dataset['title'] = dataset['title'].str.replace('- Chapinero', '', regex=False)
dataset['title'] = dataset['title'].str.replace('- Unicentro Bogotá', '', regex=False)
dataset['title'] = dataset['title'].str.replace('- Santa Bárbara', '', regex=False)
dataset['title'] = dataset['title'].str.replace('Central', '', regex=False)
dataset['title'] = dataset['title'].str.replace('- Unictro Bogotá', '', regex=False)
dataset['title'] = dataset['title'].str.replace('Ctral', '', regex=False)

# Eliminar los registros donde la ubicación sea "Funza"
dataset= dataset[dataset['location'] != 'Siberia, Funza, Cundinamarca']
dataset= dataset[dataset['location'] != 'Altos del prado, Barranquilla, Atlantico']
dataset= dataset[dataset['location'] != 'Siberia, Cota, Cundinamarca']
dataset= dataset[dataset['location'] != 'Siberia, Cota, Cundinamarca']
dataset= dataset[dataset['location'] != 'Centro, Cajicá, Cundinamarca']
dataset= dataset[dataset['location'] != 'Ruitoque, Piedecuesta, Santander']
dataset= dataset[dataset['location'] != 'San francisco, Bucaramanga, Santander']
dataset= dataset[dataset['location'] != 'El bosque, Floridablanca, Santander']
dataset= dataset[dataset['location'] != 'La punta, Funza, Cundinamarca']
dataset= dataset[dataset['location'] != 'Guamito, La ceja, Antioquia']
dataset= dataset[dataset['location'] != 'Universidad, Bucaramanga, Santander']
dataset= dataset[dataset['location'] != 'La ceja, Antioquia']
dataset= dataset[dataset['location'] != 'Guayaquil, Medellín, Antioquia']
dataset= dataset[dataset['location'] != 'Laureles, Medellín, Antioquia']
dataset= dataset[dataset['location'] != 'Niquia, Bello, Antioquia']
dataset= dataset[dataset['location'] != 'El ingenio, Cali, Valle del cauca']
dataset= dataset[dataset['location'] != 'La playa, Cúcuta, Norte de santander']
dataset= dataset[dataset['location'] != 'Mosquera, Cundinamarca']
dataset= dataset[dataset['location'] != 'Centro oriental, Cúcuta, Norte de santander']
dataset= dataset[dataset['location'] != 'El carmen de viboral, El carmen de viboral, Antioquia']
dataset= dataset[dataset['location'] != 'Guayabito, Rionegro, Antioquia']
dataset= dataset[dataset['location'] != 'Shellmar, Medellín, Antioquia']
dataset= dataset[dataset['location'] != 'San luis, Cúcuta, Norte de santander']
dataset= dataset[dataset['location'] != 'Libertadores, Cúcuta, Norte de santander']
dataset= dataset[dataset['location'] != 'Actividad multiple, Copacabana, Antioquia']

df=dataset

# Precio mínimo y máximo
min_value = df['price'].min()
max_value = df['price'].max()

# Configuración de la página
st.set_page_config(
    page_title='Expansion',
    page_icon='https://raw.githubusercontent.com/JuliethSuarezPoveda/gdp-dashboard/refs/heads/main/expansion.jfif'
)
# expansion logo
st.image('https://raw.githubusercontent.com/JuliethSuarezPoveda/gdp-dashboard/refs/heads/main/Logo.jfif')

# Slider para rango de precios
from_price, to_price = st.slider(
    'Escoja un rango de precio',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value]
)

#print(dataset['location'].unique())


# Aplicar estilos CSS para fondo morado claro y otros detalles 
st.markdown(
    """
    <style>
        /* Fondo morado claro */
        .stApp {
            background-color: #f0f0f0;
        }

        /* Estilo para el título */
        h1 {
            color: #000000;
        
        /* Texto del local a la izquierda */
        .local-details {
            flex: 1;
            padding-right: 20px;
        }


        /* Ajustar las fuentes y colores de los textos */
        .stSlider label, .stMultiSelect label {
            font-size: 18px;
            color: #000000;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# Multiselect para tipo de local
tipo_de_local = df['title'].unique()
selected_local = st.multiselect(
    '¿Qué tipo de local busca?',
    tipo_de_local,
    ['Oficina ', 'Local ', 'Bodega ']
)

# Multiselect para ubicación
ubicacion = df['location'].unique()
selected_ubicacion = st.multiselect(
    'Escoja la ubicación de su preferencia',
    ubicacion,
    ['El chico','Centro Internacional']
)

# Filtrar el dataset con las opciones seleccionadas
filtered_df = df[
    (df['price'] >= from_price) & 
    (df['price'] <= to_price) & 
    (df['title'].isin(selected_local)) & 
    (df['location'].isin(selected_ubicacion))
]

# Mostrar las opciones filtradas
if not filtered_df.empty:
    st.write(f"Mostrando {len(filtered_df)} resultados que coinciden con tus preferencias.")
    
    # Mostrar los locales y sus imágenes
    for index, row in filtered_df.iterrows():
        # Crear dos columnas: una para el texto y otra para la imagen
        col1, col2 = st.columns([2, 1])  # La primera columna (texto) será el doble del tamaño de la segunda (imagen)
        
        # Columna 1: Detalles del local
        with col1:
            st.markdown(f"""
            <strong>{row['title']}</strong> en {row['location']}<br>
            Precio: {row['price']} COP <br> Área: {row['area']} <br>
            Dirección: {row['address']}
            """, unsafe_allow_html=True)
        
        # Columna 2: Imagen del local
        with col2:
            # Cargar y mostrar la imagen desde el enlace
            try:
                response = requests.get(row['main_image'])
                response.raise_for_status()  # Levantar excepción para errores HTTP
                image = Image.open(BytesIO(response.content))
                # Mostrar la imagen con un ancho ajustado
                st.image(image, caption=f"Imagen {row['title']}", width=150)
            except requests.exceptions.RequestException:
                st.warning("Imagen no disponible")
            except Exception as e:
                st.error(f"Error al cargar la imagen: {e}")
else:
    st.warning("No se encontraron resultados para sus criterios seleccionados.")