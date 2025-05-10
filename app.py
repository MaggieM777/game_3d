import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide")
st.title("3D модел с .obj във Streamlit")

# Зареждане на HTML + Three.js визуализация
with open("viewer.html", "r") as f:
    html_code = f.read()

# Показване на вградения viewer
components.html(html_code, height=600)
