import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

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

# Voy a cambiar la columna de condition a números para poder graficar.

df["condition"] = df["condition"].replace("salvage", "1")
df["condition"] = df["condition"].replace("fair", "3")
df["condition"] = df["condition"].replace("good", "5")
df["condition"] = df["condition"].replace("like new", "7")
df["condition"] = df["condition"].replace("excellent", "9")
df["condition"] = df["condition"].replace("new", "10")
df["condition"] = df["condition"].astype(int)

# La columna date_posted debería de ser tipo datetime y no object
df["date_posted"] = pd.to_datetime(df["date_posted"])


# Aplicación Web con Streamlit
# Titulos y descripción de la web
st.markdown("<p style='font-size:40px; text-align:center;'>Bienvenido a Auto Fácil 🚗.</p>",
            unsafe_allow_html=True)
st.markdown("<p style='font-size:18px; text-align:justify;'>Hola, mi nombre es Alejandro Aguirre y soy el fundador de Auto Fácil ©. Aquí podrás encontrar entre muchos de nuestros autos en excelentes condiciones, tenemos autos nuevos, semi-nuevos y reparados. Utiliza nuestro buscador para encontrar el mejor modelo para ti. Puedes agendar una cita de manejo para conocer el próximo auto de tus sueños.</p>", unsafe_allow_html=True)

# Slide de imágenes
images = [
    "https://i.pinimg.com/originals/7d/67/77/7d677755f926da011c6b2ef44ad92aaa.jpg",
    "https://i.ytimg.com/vi/e8SEyZHXb_g/maxresdefault.jpg",
    "https://dealerscloud.blob.core.windows.net/leesburgautoimport/1C3CCCAG1HN502472/800/1.jpg",
    "https://i.ytimg.com/vi/BHUlqKkRfAQ/maxresdefault.jpg",
    "https://acnews.blob.core.windows.net/imgnews/large/0_30165525849.jpg",
    "https://st2.stat.vin/files/1N4AL3APXEC409160/COPART/30265051/photo/4acfc87d-556a-40ac-9251-db29cd629f34.jpg",
    "https://i.ebayimg.com/thumbs/images/g/AN4AAOSwoxdnlXOk/s-l1200.jpg"]

indice = st.slider(
    "Estos son algunos de nuestros modelos disponibles", 0, len(images) - 1, 0)
st.image(images[indice],
         caption=f"Modelo {indice + 1}", use_container_width=True)

# Histograma y diagrama de dispersión
var = st.selectbox('Selecciona el parámetro para el histograma', [
    "Precio", "Año", "Kilometraje"])
hist_button = st.button(
    'Puedes generar un histograma en base a el parámetro que desees')
if hist_button:
    if var == "Precio":
        var = "price"
        fig = px.histogram(df, x=var, labels={
                           var: "Precio"}, title="Histograma de precios")
        st.plotly_chart(fig, use_container_width=True)
    if var == "Año":
        var = "model_year"
        fig = px.histogram(df, x=var, labels={
                           var: "Año del modelo"}, title="Histograma de Años del modelo")
        st.plotly_chart(fig, use_container_width=True)
    if var == "Kilometraje":
        var = "odometer"
        fig = px.histogram(df, x=var, labels={
                           var: "Kilometraje"}, title="Histograma de Kilometraje")
        st.plotly_chart(fig, use_container_width=True)

var_1 = st.selectbox('Selecciona los parámetros para la gráfica de dispersión (x,y)', [
    "Precio - Condición", "Año - Condición", "Kilometraje - Condición"])

scatter_button = st.button('Construye un diagrama de dispersión')
if scatter_button:
    legend_conditions = {
        10: "Nuevo",
        9: "Excelente",
        7: "Como nuevo",
        5: "Bueno",
        3: "Regular",
        1: "Reparado por accidente"
    }

    if var_1 == "Precio - Condición":
        fig = px.scatter(df, x="price", y="condition",
                         labels={"price": "Precio",
                                 "condition": "Condición del carro"},
                         title="Diagrama de dispersión entre Precio y Condición")
        for valor, etiqueta in legend_conditions.items():
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(
                size=10), name=f"{valor} - {etiqueta}"))
        st.plotly_chart(fig, use_container_width=True)
    if var_1 == "Año - Condición":
        fig = px.scatter(df, x="model_year", y="condition",
                         labels={"model_year": "Año del Modelo",
                                 "condition": "Condición"},
                         title="Diagrama de dispersión entre Año del Modelo y Condición")
        for valor, etiqueta in legend_conditions.items():
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(
                size=10), name=f"{valor} - {etiqueta}"))
        st.plotly_chart(fig, use_container_width=True)
    if var_1 == "Kilometraje - Condición":
        fig = px.scatter(df, x="odometer", y="condition",
                         labels={"odometer": "Kilometraje",
                                 "condition": "Condición"},
                         title="Diagrama de dispersión entre Kilometraje y Condición")
        for valor, etiqueta in legend_conditions.items():
            fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(
                size=10), name=f"{valor} - {etiqueta}"))
        st.plotly_chart(fig, use_container_width=True)

# Contacto
st.markdown("<p style='font-size:18px; text-align:justify;'>Ven a conocer tu auto.</p>",
            unsafe_allow_html=True)
with st.form("Agendar cita"):
    nombre = st.text_input("Tu nombre")
    correo = st.text_input("Tu correo")
    mensaje = st.text_area("Mensaje al vendedor")
    enviado = st.form_submit_button("Enviar")
    if enviado:
        st.success(
            "Nosotros nos pondremos en contacto contigo pronto, muchas gracias por su preferencia.")
