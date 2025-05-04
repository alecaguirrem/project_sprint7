import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv("vehicles_us.csv")

st.header('Análisis de anuncios de venta de coches')
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
