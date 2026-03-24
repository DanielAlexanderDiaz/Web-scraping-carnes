import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from math import ceil

st.set_page_config(page_title="Carnes CL", layout="wide", page_icon="🥩")

st.title("Agrocomercial")
st.link_button("Sitio web - Agrocomercial", "https://agrocomercial.cl/")
st.divider()


nombre_tienda = 'agrocomercial'
state = st.session_state

if 'categoria' not in state:
    state.categoria = []
if 'nombre' not in state:
    state.nombre = ""  
if 'tienda' not in state:
    state.tienda = []
if 'df_filtro' not in state:
    state.df_filtro = None

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
    
    c1, c2, c3 = st.columns(3)
    with c1:
        nombre = st.text_input("Nombre del producto", value=state.nombre)
        if nombre!=state.nombre:
            state.nombre = nombre   
    with c2:
        categoria = st.multiselect("Categorias", ['vacuno', 'pollo', 'cerdo', 'cordero', 'pavo']) 
        if categoria!=state.categoria:
            state.categoria = categoria
    with c3:
        tienda = st.multiselect("Tiendas", ['agrocomercial'])
        if tienda!=state.tienda:
            state.tienda = tienda

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
            print(f"Error en {nombre_tienda} {clean_url}: {e}")
        
        progress_bar.progress((i + 1) / total_urls)
        status_text.text(f"{nombre_tienda} en proceso... ({i + 1}/{total_urls})")
    
    status_text.text(f"Operacion completada en {nombre_tienda}")
    progress_bar.progress(1.0)
    
    if all_agro_data:
        df_macro = pd.DataFrame(all_agro_data,columns=['Tienda','Categoria','nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        df_limpio = df_macro.drop_duplicates(keep='first')
        
        columnas_numericas = ['precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total']
        df_limpio[columnas_numericas] = df_limpio[columnas_numericas].apply(pd.to_numeric, errors='coerce')
          
        state.df_filtro = df_limpio  
            
    else:
        st.warning(f"No se encontraron datos en {nombre_tienda}")
        state.df_filtro = None
        
if state.df_filtro is not None:
    df = state.df_filtro.copy()
    
    filtro_categoria = state.categoria  
    filtro_nombre = state.nombre.strip()
    filtro_tienda = state.tienda 
    
    df_display = df 
    
    if filtro_nombre:
        mask_nombre = (
            df['nombre_simple'].str.contains(filtro_nombre, case=False, na=False) |
            df['nombre_corto'].str.contains(filtro_nombre, case=False, na=False) |
            df['nombre_largo'].str.contains(filtro_nombre, case=False, na=False)
        )
        df_display = df_display[mask_nombre]
    
    if filtro_categoria and len(filtro_categoria) > 0:
        df_display = df_display[df_display['Categoria'].isin(filtro_categoria)]
        
    if filtro_tienda and len(filtro_tienda) > 0:
        df_display = df_display[df_display['Tienda'].isin(filtro_tienda)]
    
    if not df_display.empty:
        st.dataframe(
            df_display.sort_values('precio_neto_kg', ascending=True),
            width='stretch',
            hide_index=True
        )
    else:
        st.warning("No se encontraron productos con los filtros seleccionados", icon="⚠️")