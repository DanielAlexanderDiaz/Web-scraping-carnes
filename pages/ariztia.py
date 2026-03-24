import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from math import ceil

st.set_page_config(page_title="Carnes CL", layout="wide", page_icon="🥩")

st.title("Ariztía")
st.link_button("Sitio web - ariztia", "https://www.ariztiaatucasa.cl/")
st.divider()

nombre_tienda = 'ariztia'


def extract_ariztia(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('strong', class_='product-item-name')

        for producto in productos:
            link_tag = producto.find('a', class_='product-item-link')
            if not link_tag:
                continue
            nombre_producto = link_tag.text.strip()

            # Limpiar "aprox." y puntos innecesarios
            texto_limpio = re.sub(r'\baprox\.?|\.', '', nombre_producto, flags=re.IGNORECASE).strip()

            # Extraer nombre, cantidad y unidad
            patron_nombre = re.compile(r'^(.*?)\s+(\d+(?:[.,]\d+)?)\s*(kg|gr)\b', re.IGNORECASE)
            match_nombre = patron_nombre.search(texto_limpio)
            if not match_nombre:
                continue

            nombre = match_nombre.group(1).strip()
            cantidad = match_nombre.group(2)
            unidad = match_nombre.group(3).lower()

            # Buscar el precio por kg
            precio_origen = producto.find('span', class_='precio-kilo')
            if not precio_origen:
                continue

            precio_texto = precio_origen.get_text()
            patron_precio = re.compile(r'\$(\d+\.\d+)\s*kg', re.IGNORECASE)
            match_precio = patron_precio.search(precio_texto)
            if not match_precio:
                continue

            numero_str = match_precio.group(1)
            valor_limpio = numero_str.replace('.', '')
            valor_numerico = int(valor_limpio)

            precio_neto_kg = int(valor_numerico / 1.19)
            
            p = r'(?i)\b(de Pollo|de Vacuno|IQF|Fresco|Congelada|Congelado|2 Un|al vacío|envasado|envasada|Caja de|Granel|granel|Ariztia|Caja|Congeladas|Fresca|de Pavo|porcionada|de Cerdo|al Vacio|envase|Light|.)\b\.?\s*'
            
            nombre_largo = nombre_producto
            nombre_corto = nombre
            nombre_simple = re.sub(p,' ', nombre_corto)
            precio_neto_total = 0 
            precio_bruto_kg = valor_numerico
            precio_bruto_total = 0
            
            try:      
                if nombre_simple != 'sin data':          
                    data.append([
                                nombre_tienda,
                                categoria,
                                nombre_largo.lstrip(), 
                                nombre_corto.lstrip(), 
                                nombre_simple.lstrip(),
                                precio_neto_kg, 
                                precio_neto_total, 
                                precio_bruto_kg, 
                                precio_bruto_total
                                ])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre_largo} - {e}")
                continue
                        
        print(f"Datos extraídos de Ariztía: {url}")
    else:
        print(f"Error al acceder a Ariztía {url}. Código: {response.status_code}")

    return data

if st.button("Extraer datos"):
    
    categorias = {
        'pollo.html':'pollo',
        'pollo.html?p=2':'pollo',
        'pollo.html?p=3':'pollo',
        'pollo.html?p=4':'pollo',
        'pollo.html?p=5':'pollo',
        'pollo.html?p=6':'pollo',
        'pavo.html':'pavo',
        'pavo.html?p=2':'pavo',
        'cerdo.html':'cerdo',
        'vacuno.html':'vacuno',
        'vacuno.html?p=2':'vacuno',
        'congelados/hamburguesas.html':'congelados',
        'congelados/productos-churrasco-lomito-y-bistec.html':'congelados',
        'congelados/nuggets-y-apanados.html':'congelados',
    }
    
    urls_agro = list(categorias.keys())
    total_urls = len(urls_agro)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    base_agro = 'https://www.ariztiaatucasa.cl/'
    all_agro_data = []
    
    for i, url in enumerate(urls_agro):
        clean_url = f"{base_agro}{url.strip()}"
        categoria = categorias.get(url, 'sin categoria')
        try:
            all_agro_data.extend(extract_ariztia(clean_url, categoria))
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
          
        # state.df_filtro = df_limpio  
        
        st.dataframe(df_limpio)
            
    else:
        st.warning(f"No se encontraron datos en {nombre_tienda}")
        # state.df_filtro = None