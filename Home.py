import streamlit as st

st.set_page_config(page_title="GPT Home", page_icon="🧊")

with st.sidebar:
    st.title("title")

st.title("GPT Home")
tabs = st.tabs(["A", "B", "C"])

with tabs[0]:
    st.write("a")

with tabs[1]:
    st.write("b")

with tabs[2]:
    st.write("c")
