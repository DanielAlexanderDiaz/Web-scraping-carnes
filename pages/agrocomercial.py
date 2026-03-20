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

if 'df_macro' not in st.session_state:
    st.session_state.df_macro = None  
if 'filtro_categoria' not in st.session_state:
    st.session_state.filtro_categoria = '' 
if 'filtro_nombre' not in st.session_state:
    st.session_state.filtro_nombre = ''   

# === FUNCIÓN DE FILTRADO ===
def aplicar_filtros(df, categoria, nombre):
    """Filtra el dataframe según los términos ingresados"""
    if df is None or df.empty:
        return df
    
    df_f = df.copy()
    
    if categoria:
        df_f = df_f[df_f['Categoria'].str.contains(categoria, case=False, na=False)]
    
    if nombre:
        df_f = df_f[df_f['nombre_simple'].str.contains(nombre, case=False, na=False)]
    
    return df_f

def extract_agrocomercial(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        categoria = soup.find('div', class_='et_pb_heading_container').text
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
                    data.append([nombre_sitio, categoria, nombre_largo, nombre_corto, nombre_simple,f'{precio_neto_kg:.0f}', f'{precio_neto_total:.0f}', f'{precio_bruto_kg:.0f}', f'{precio_bruto_total:.0f}'])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
            
        print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")

    return data

if st.button("Extraer datos"):
    urls_agro = ['vacuno/','aves/pollo/','cerdo/','cordero/','aves/pavo/','vacuno/elaborados/','detalle/']
    total_urls = len(urls_agro)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    base_agro = 'https://agrocomercial.cl/product-category/'
    all_agro_data = []
    
    for i, url in enumerate(urls_agro):
        clean_url = f"{base_agro}{url.strip()}"
        try:
            all_agro_data.extend(extract_agrocomercial(clean_url))
        except Exception as e:
            print(f"Error en Agrocomercial {clean_url}: {e}")
        
        progress_bar.progress((i + 1) / total_urls)
        status_text.text(f"Operacion en proceso... ({i + 1}/{total_urls})")
    
    status_text.text("Operacion completada. ✅")
    progress_bar.progress(1.0)
    
    if all_agro_data:
        # Crear dataframe y guardar en session_state
        df_macro = pd.DataFrame(all_agro_data,columns=['Tienda','Categoria', 'nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        
        st.session_state.df_macro = df_macro  # ✅ Persistir dataframe
        st.rerun()  # ✅ Refrescar para mostrar filtros y datos
    else:
        st.warning("No se encontraron datos en Agrocomercial. ⚠️")

if st.session_state.df_macro is not None:
    
    with st.container(horizontal=True):
        categoria_input = st.text_input("Filtrar por Categoría",value=st.session_state.filtro_categoria,placeholder="Ej: Vacuno, Pollo...",key="input_categoria")
        st.session_state.filtro_categoria = categoria_input
    
        nombre_input = st.text_input("Filtrar por Nombre", value=st.session_state.filtro_nombre,placeholder="Ej: posta, filete...",key="input_nombre")
        st.session_state.filtro_nombre = nombre_input
    
    df_filtrado = aplicar_filtros(st.session_state.df_macro,st.session_state.filtro_categoria,st.session_state.filtro_nombre)
    
    if st.session_state.filtro_categoria or st.session_state.filtro_nombre:
        st.caption(f"🔹 Filtros activos: Categoría='{st.session_state.filtro_categoria}' | Nombre='{st.session_state.filtro_nombre}' → {len(df_filtrado)} resultados")
    
    st.dataframe(df_filtrado.sort_values('precio_neto_kg', ascending=False),hide_index=True)
    
    # 🔹 TU GROUBY ORIGINAL (con datos filtrados)
    productos_categorias = df_filtrado.groupby('Categoria')['Tienda'].count().reset_index(name='Total')
    st.dataframe(productos_categorias,hide_index=True)
    
    st.text(f"Total de productos: {len(df_filtrado)}")

else:
    st.info("👈 Presiona 'Extraer datos' para comenzar.")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    