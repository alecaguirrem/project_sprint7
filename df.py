import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_csv(
    "C:/Users/aaguirre/Documents/Alejandro Aguirre/Personal/Curso Python/TT_Sprint7/project_sprint7/vehicles_us.csv")

# La columan Model year debería de ser tipo object y no float, los datos ausentes serán "unknown".

df["model_year"] = df["model_year"].fillna(0)
df["model_year"] = df["model_year"].astype(int)
df["model_year"] = df["model_year"].astype(str)
df["model_year"] = df["model_year"].replace(0, "unknown")

# La columan de cylinders debería de ser tipo str y no float.

df["cylinders"] = df["cylinders"].fillna(0)
df["cylinders"] = df["cylinders"].astype(int)
df["cylinders"] = df["cylinders"].astype(str)
df["cylinders"] = df["cylinders"].replace(0, "unknown")

# La columna odometer debería de ser tipo str y no float.

df["odometer"] = df["odometer"].fillna(0)
df["odometer"] = df["odometer"].astype(int)
df["odometer"] = df["odometer"].astype(str)
df["odometer"] = df["odometer"].replace(0, "unknown")

# En la columna type aparece SUV en mayíusculas lo cambiaré a minúsculas

df["type"] = df["type"].str.lower()

# La columna paint_color llenaré con unknown los datos ausentes

df["paint_color"] = df["paint_color"].fillna("unknown")

# En la columna is_4wd hay algunos tipos de carros que no pueden tener más de 4 ruedas, como los suvs,
# sedanes, copues, etc. Por lo que los llenaré con 1 (es 4wd) y los demás con 0).

four_wheels = ["suv", "sedan", "coupe", "convertible", "hatchback", "wagon"]

df.loc[(df['type'].isin(four_wheels)) & (df['is_4wd'].isna()), 'is_4wd'] = 1
df["is_4wd"] = df["is_4wd"].fillna(0)
df["is_4wd"] = df["is_4wd"].astype(int)

# La columna date_posted debería de ser tipo datetime y no object
df["date_posted"] = pd.to_datetime(df["date_posted"])
