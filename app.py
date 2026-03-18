import streamlit as st

pages = {
    "": [
        st.Page("pages/todo.py", title="Todos los sitios web"),
    ],
    "Sitios web": [
        st.Page("pages/agrocomercial.py", title="Agrocomercial"),
    ]
}

pg = st.navigation(pages,position="top")
pg.run()
