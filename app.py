import streamlit as st

# st.set_page_config(
#     page_title="Ex-stream-ly Cool App",
#     page_icon="🧊",
#     layout="wide",
#     initial_sidebar_state="expanded",
#     menu_items={
#         'Get Help': 'https://www.extremelycoolapp.com/help',
#         'Report a bug': "https://www.extremelycoolapp.com/bug",
#         'About': "# This is a header. This is an *extremely* cool app!"
#     }
# )

pages = {
    "": [
        st.Page("pages/todo.py", title="Todos los sitios"),
    ],
    "Tiendas": [
        st.Page("pages/agrocomercial.py", title="Agrocomercial"),
    ]
}

pg = st.navigation(pages,position="top")
pg.run()
