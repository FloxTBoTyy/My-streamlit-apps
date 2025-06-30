import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# Configuración de la app
st.set_page_config(page_title="ML Trainer Penguins", layout="centered")
st.title("🧠 Entrenador de modelo ML con datos penguin 🐧")

# Cargar dataset más complejo
penguins = sns.load_dataset("penguins")

# Limpiar datos
penguins = penguins.dropna(subset=["species"])  # quitar filas sin target
penguins = penguins.drop(columns=["island", "sex"])  # quitar columnas categóricas sin codificar
penguins = penguins.dropna()  # quitar filas con nulos

X = penguins.drop("species", axis=1)
y = penguins["species"]

# Codificar y (target)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
class_names = label_encoder.classes_

# ---------------- Sidebar: modelo e hiperparámetros ---------------- #
st.sidebar.header("🎛️ Configura el modelo")

modelo_seleccionado = st.sidebar.selectbox("Modelo a usar", ["Random Forest", "KNN"])

if modelo_seleccionado == "Random Forest":
    n_estimators = st.sidebar.slider("n_estimators", 10, 200, 100, step=10)
    max_depth = st.sidebar.slider("max_depth", 1, 20, 5)
elif modelo_seleccionado == "KNN":
    n_neighbors = st.sidebar.slider("n_neighbors", 1, 15, 5)

# ---------------- Entrenamiento ---------------- #
if "modelo_entrenado" not in st.session_state:
    st.session_state.modelo_entrenado = None
    st.session_state.X_test = None
    st.session_state.y_test = None
    st.session_state.y_pred = None

if st.button("🚀 Entrenar modelo"):
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.3, random_state=42)

    if modelo_seleccionado == "Random Forest":
        modelo = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    elif modelo_seleccionado == "KNN":
        modelo = KNeighborsClassifier(n_neighbors=n_neighbors)

    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    st.session_state.modelo_entrenado = modelo
    st.session_state.X_test = X_test
    st.session_state.y_test = y_test
    st.session_state.y_pred = y_pred

    st.success("✅ Modelo entrenado con éxito")

# ---------------- Predicción manual ---------------- #
if st.session_state.modelo_entrenado:
    st.subheader("🔍 Predicción con nueva fila")

    input_data = []
    for feature in X.columns:
        val = st.number_input(f"{feature}", value=float(X[feature].mean()), format="%.2f")
        input_data.append(val)

    if st.button("🎯 Predecir"):
        pred = st.session_state.modelo_entrenado.predict([input_data])[0]
        st.info(f"Resultado: **{class_names[pred]}**")

    # ---------------- Métricas ---------------- #
    st.subheader("📊 Métricas del modelo")

    acc = accuracy_score(st.session_state.y_test, st.session_state.y_pred)
    prec = precision_score(st.session_state.y_test, st.session_state.y_pred, average="macro")
    rec = recall_score(st.session_state.y_test, st.session_state.y_pred, average="macro")
    cm = confusion_matrix(st.session_state.y_test, st.session_state.y_pred)

    st.write(f"**Accuracy:** {acc:.2f}")
    st.write(f"**Precision:** {prec:.2f}")
    st.write(f"**Recall:** {rec:.2f}")

    st.write("**Matriz de Confusión:**")
    fig, ax = plt.subplots()
    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicho")
    plt.ylabel("Verdadero")
    st.pyplot(fig)
else:
    st.info("⚠️ Entrena el modelo primero para hacer predicciones o ver métricas.")
