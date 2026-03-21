import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from math import ceil

st.set_page_config(layout="wide")

st.title("Agrocomercial")
st.link_button("Sitio web - Agrocomercial", "https://agrocomercial.cl/")
st.divider()

if 'categoria_filtro' not in st.session_state:
    st.session_state.categoria_filtro = 'sin categoria'
if 'df_filtro' not in st.session_state:
    st.session_state.df_filtro = None

def extract_agrocomercial(url, categoria='sin categoria'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('li', class_='status-publish')
        nombre_sitio = 'agrocomercial'

        for producto in productos:
            solo_nombre = 'sin data'
            kg = 1

            nombre_tag = producto.find('h2', class_='woocommerce-loop-product__title')
            if not nombre_tag:
                continue
            nombre = nombre_tag.text.strip()

            patron = r'^(.*?)\s+(\d+(?:\.\d+)?)\s*[kK][gG]\b'
            match = re.match(patron, nombre)
            if match:
                solo_nombre = match.group(1).strip()
                kg = match.group(2)

            precio_final = None
            ins_tag = producto.find('ins')
            if ins_tag:
                precio_final = ins_tag.get_text(strip=True).replace('$', '').replace('.', '')
            else:
                span_precio = producto.find('span', class_='woocommerce-Price-amount')
                if span_precio:
                    precio_final = span_precio.get_text(strip=True).replace('$', '').replace('.', '')
                else:
                    continue  # Saltar si no hay precio

            try:
                p = r'(?i)\b(CAT-V|Caja|CONGELADO|Vacio|Porc.|Vacuno|de Vacuno|de Cerdo|Porc|Cat V|de Pollo|Cajas de|Porcionada|Porcionado|2.0 aprox|Congelada|Fresca|.)\b\.?\s*'
                
                kg_int = int(kg)
                precio_bruto_total = int((precio_final))
                precio_bruto_kg = ceil(precio_bruto_total/kg_int)
                precio_neto_total = ceil(precio_bruto_total/1.19)
                precio_neto_kg = ceil(precio_bruto_kg/1.19)
                nombre_largo = f"{solo_nombre}, {kg} kg"
                nombre_corto = f"{solo_nombre}"
                nombre_simple = re.sub(p, ' ', solo_nombre)
                
                if solo_nombre != 'sin data':
                    data.append([
                        nombre_sitio,
                        categoria,
                        nombre_largo, 
                        nombre_corto, 
                        nombre_simple,
                        precio_neto_kg, 
                        precio_neto_total, 
                        precio_bruto_kg, 
                        precio_bruto_total
                        ])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
            
        print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")

    return data

with st.container(border=True):
    
    filtro_input = st.text_input("Filtrar por categoría", placeholder="vacuno, pollo, cerdo, cordero, pavo ...", value=st.session_state.categoria_filtro)
    
    if filtro_input!=st.session_state.categoria_filtro:
        st.session_state.categoria_filtro = filtro_input
        
    if st.button("Limpiar filtro"):
        st.session_state.categoria_filtro = 'sin categoria'
        st.rerun() 

if st.button("Extraer datos"):
    
    categorias = {
        'vacuno/':'vacuno',
        'aves/pollo/':'pollo',
        'cerdo/':'cerdo',
        'cordero/':'cordero',
        'aves/pavo/':'pavo'
    }
    
    urls_agro = list(categorias.keys())
    total_urls = len(urls_agro)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    base_agro = 'https://agrocomercial.cl/product-category/'
    all_agro_data = []
    
    for i, url in enumerate(urls_agro):
        clean_url = f"{base_agro}{url.strip()}"
        categoria = categorias.get(url, 'sin categoria')
        try:
            all_agro_data.extend(extract_agrocomercial(clean_url, categoria))
        except Exception as e:
            print(f"Error en Agrocomercial {clean_url}: {e}")
        
        progress_bar.progress((i + 1) / total_urls)
        status_text.text(f"Operacion en proceso... ({i + 1}/{total_urls})")
    
    status_text.text("Operacion completada. ✅")
    progress_bar.progress(1.0)
    
    if all_agro_data:
        df_macro = pd.DataFrame(all_agro_data,columns=['Tienda','Categoria','nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        df_limpio = df_macro.drop_duplicates(keep='first')
        
        columnas_numericas = ['precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total']
        df_limpio[columnas_numericas] = df_limpio[columnas_numericas].apply(pd.to_numeric, errors='coerce')
          
        st.session_state.df_filtro = df_limpio  
            
    else:
        st.warning("No se encontraron datos en Agrocomercial.")
        st.session_state.df_filtro = None
        
if st.session_state.df_filtro is not None:
    df = st.session_state.df_filtro.copy()
    
    filtro = st.session_state.categoria_filtro.strip().lower()
    
    if filtro != 'sin categoria':
        
        df_limpio = df[df['Categoria'].str.contains(filtro, case=False, na=False)]
        
        if len(df_limpio)==0:
           st.warning(f"⚠️ No se encontraron datos para la categoría: {filtro}")
           st.info("Intenta con otra categoría")
        else:
            st.success(f"✅ Se encontraron {len(df_limpio)} productos para la categoría: {filtro}")
            df_display = df_limpio 
    else:
        df_display = df
        
    st.dataframe(df_display.sort_values('precio_neto_kg'), width='stretch', hide_index=True)