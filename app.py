import streamlit as st

pages = {
    "": [
        st.Page("pages/todo.py", title="Todos los sitios web"),
        st.Page("pages/scraping.py", title="scraping"),
    ],
}

pg = st.navigation(pages,position="top")
pg.run()
