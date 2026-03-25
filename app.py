import streamlit as st

pages = {
    "": [
        st.Page("pages/todo.py", title="Todos los sitios web"),
    ],
}

pg = st.navigation(pages,position="top")
pg.run()
