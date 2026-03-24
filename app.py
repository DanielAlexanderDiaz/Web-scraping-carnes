import streamlit as st

pages = {
    "": [
        st.Page("pages/todo.py", title="Todos los sitios web"),
    ],
    "Sitios web": [
        st.Page("pages/agrocomercial.py", title="Agrocomercial"),
        st.Page("pages/ariztia.py", title="ariztia"),
    ]
}

pg = st.navigation(pages,position="top")
pg.run()
