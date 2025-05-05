import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("vehicles_us.csv")

# Ordenamiento del df y conversión de tipos de datos
# La columan Model year debería de ser tipo object y no float, los datos ausentes serán "unknown".

df["model_year"] = df["model_year"].fillna(0)
df["model_year"] = df["model_year"].astype(int)
df["model_year"] = df["model_year"].astype(str)
df["model_year"] = df["model_year"].replace("0", "unknown")

# La columan de cylinders debería de ser tipo str y no float.

df["cylinders"] = df["cylinders"].fillna(0)
df["cylinders"] = df["cylinders"].astype(int)
df["cylinders"] = df["cylinders"].astype(str)
df["cylinders"] = df["cylinders"].replace("0", "unknown")

# La columna odometer debería de ser tipo str y no float.

df["odometer"] = df["odometer"].fillna(0)
df["odometer"] = df["odometer"].astype(int)
df["odometer"] = df["odometer"].astype(str)
df["odometer"] = df["odometer"].replace("0", "unknown")

# En la columna type aparece SUV en mayíusculas lo cambiaré a minúsculas

df["type"] = df["type"].str.lower()

# La columna paint_color llenaré con unknown los datos ausentes

df["paint_color"] = df["paint_color"].fillna("unknown")

# En la columna is_4wd hay algunos tipos de carros que no pueden tener más de 4 ruedas, como los suvs,
# sedanes, copues, etc. Por lo que los llenaré con 1 (es 4wd) y los demás con 0).

four_wheels = ["suv", "sedan", "coupe", "convertible", "hatchback", "wagon"]

df["is_4wd"] = df["is_4wd"].astype(object)
df["is_4wd"] = df["is_4wd"].replace(1.0, "yes")
df.loc[(df['type'].isin(four_wheels)) & (
    df['is_4wd'].isna()), 'is_4wd'] = "yes"
df["is_4wd"] = df["is_4wd"].fillna("unknown")

# La columna date_posted debería de ser tipo datetime y no object
df["date_posted"] = pd.to_datetime(df["date_posted"])

# Aplicación Web con Streamlit
# Tpitulos y descripción de la web
st.header('Bienvenido a Auto Fácil 🚗.',)
st.markdown("<p style='font-size:40px; text-align:center;'>Bienvenido a Auto Fácil 🚗.</p>",
            unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; text-align:justify;'>Hola, mi nombre es Alejandro Aguirre y soy el fundador de Auto Fácil ©. Aquí podrás encontrar entre muchos de nuestros autos en excelentes condiciones, tenemos autos nuevos, semi-nuevos y usados. Utiliza nuestro buscador para encontrar el mejor modelo para ti. Puedes agendar una cita de manejo para conocer el próximo auto de tus sueños.</p>", unsafe_allow_html=True)

# Slide de imágenes
images = [
    "https://static.cargurus.com/images/forsale/2025/04/04/04/05/2002_honda_civic-pic-2171495440266185037-1024x768.jpeg",
    "https://i.ytimg.com/vi/e8SEyZHXb_g/maxresdefault.jpg",
    "https://dealerscloud.blob.core.windows.net/leesburgautoimport/1C3CCCAG1HN502472/800/1.jpg",
    "https://static.cargurus.com/images/forsale/2025/04/24/19/28/2013_nissan_maxima-pic-8675347025972541598-1024x768.jpeg",
    "https://acnews.blob.core.windows.net/imgnews/large/0_30165525849.jpg",
]

indice = st.slider("Desliza para ver modelos", 0, len(images) - 1, 0)
st.image(images[indice], caption=f"Modelo {indice + 1}", use_column_width=True)

hist_button = st.button('Construye un histograma')
if hist_button:
    st.write(
        'Creación de un histograma para el conjunto de datos de anuncios de venta de coches')
    fig = px.histogram(df, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

scatter_button = st.button('Construye un diagrama de dispersión')
if scatter_button:
    st.write('Creación de diagrama de dispersión para el conjunto de datos de anuncios de venta de coches')
    fig = px.scatter(df, x="odometer")
    st.plotly_chart(fig, use_container_width=True)

print("hola")
