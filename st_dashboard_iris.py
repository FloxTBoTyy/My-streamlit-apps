import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Configuración de página
st.set_page_config(page_title="Iris Dashboard", layout="wide")

# Cargar datos
iris = load_iris(as_frame=True)
df = iris.frame
df['target'] = df['target'].map(dict(enumerate(iris.target_names)))

# Sidebar – Filtro
species = st.sidebar.multiselect(
    "Selecciona especie:",
    options=df['target'].unique(),
    default=df['target'].unique()
)

df_filtered = df[df['target'].isin(species)]

# Título
st.title("🌸 Dashboard de Datos Iris")

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total muestras", len(df_filtered))
col2.metric("Promedio Sepal Length", round(df_filtered["sepal length (cm)"].mean(), 2))
col3.metric("Promedio Sepal Width", round(df_filtered["sepal width (cm)"].mean(), 2))

st.markdown("---")

# Gráficas
col4, col5 = st.columns(2)

with col4:
    st.subheader("📊 Dispersión: Sepal Length vs Sepal Width")
    fig1, ax1 = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="sepal length (cm)",
        y="sepal width (cm)",
        hue="target",
        palette="Set2",
        ax=ax1
    )
    st.pyplot(fig1)

with col5:
    st.subheader("📈 Distribución de Petal Length")
    fig2, ax2 = plt.subplots()
    sns.histplot(
        data=df_filtered,
        x="petal length (cm)",
        hue="target",
        element="step",
        stat="density",
        common_norm=False,
        palette="Set2",
        ax=ax2
    )
    st.pyplot(fig2)

st.markdown("---")

# Tabla
st.subheader("🧾 Datos filtrados")
st.dataframe(df_filtered, use_container_width=True)
