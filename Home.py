import streamlit as st

st.title("Hello, world!")
st.subheader("Welcome to Streamlit")
st.markdown("""
    #### I love it.
""")


class A:
    def __init__(self):
        pass


1
2
3
st.write("abc")
st.write([1, 2, 3])
st.write((1, 2, 3))
st.write({"a": None, "b": set([1, 2, 3]), "c": st.title})
st.write(A)
st.write(st)
st.write("a", None, True, False)
