import streamlit as st

st.title("Streamlit Test")

st.write("Hello! My Streamlit application is working.")

name = st.text_input("Enter your name")

if name:
    st.success(f"Welcome {name}!")