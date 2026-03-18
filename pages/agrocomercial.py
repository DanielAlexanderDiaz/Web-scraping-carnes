import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

st.title("Agrocomercial")
st.link_button("Sitio web - Agrocomercial", "https://agrocomercial.cl/")
st.divider()

def extract_agrocomercial(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        categoria = soup.find('div', class_='et_pb_heading_container').text
        productos = soup.find_all('li', class_='status-publish')

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
                precio_bruto_kg = (precio_bruto_total/kg_int)
                precio_neto_total = (precio_bruto_total/1.19)
                precio_neto_kg = (precio_bruto_kg/1.19)
                nombre_largo = f"{solo_nombre}, {kg} kg"
                nombre_corto = f"{solo_nombre}"
                nombre_simple = re.sub(p, ' ', solo_nombre)
                if solo_nombre != 'sin data':
                    data.append([categoria, nombre_largo, nombre_corto, nombre_simple,f'{precio_neto_kg:.0f}', f'{precio_neto_total:.0f}', f'{precio_bruto_kg:.0f}', f'{precio_bruto_total:.0f}'])
                    # print(f"""
                    #       Categoria: {categoria},
                    #       nombre_largo: {nombre_largo}, 
                    #       nombre_corto: {nombre_corto}, 
                    #       nombre_simple: {nombre_simple},
                    #       precio_neto_kg: {precio_neto_kg:.0f}, 
                    #       precio_neto_total: {precio_neto_total:.0f}, 
                    #       precio_bruto_kg: {precio_bruto_kg:.0f}, 
                    #       precio_bruto_total: {precio_bruto_total:.0f}""")
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
            
        print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")

    return data

if st.button("Extraer datos"):
    # === Contar URLs totales ===
    urls_agro = ['vacuno/','aves/pollo/','cerdo/','cordero/','aves/pavo/','vacuno/elaborados/','detalle/']

    total_urls = (len(urls_agro))
    # === Inicializar barra de progreso ===
    progress_bar = st.progress(0)
    status_text = st.empty()
    current_step = 0

    # === Agrocomercial ===
    base_agro = 'https://agrocomercial.cl/product-category/'
    all_agro_data = []
    for url in urls_agro:
        clean_url = f"{base_agro}{url.strip()}"
        try:
            all_agro_data.extend(extract_agrocomercial(clean_url))
        except Exception as e:
            print(f"Error en Agrocomercial {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Operacion en proceso. Por favor esperar... ({current_step}/{total_urls})")
        
    # === Finalizar ===
    barra = status_text.text("Operacion completada. ✅")
    progress_bar.progress(1.0)

    # === Mostrar resultados en tabs ===
    if all_agro_data:
        # df = pd.DataFrame(all_agro_data, columns=['Categoria', 'Nombre', 'Precio'])
        df = pd.DataFrame(all_agro_data, columns=['Categoria', 'nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        st.dataframe(df, width='stretch', hide_index=True)
    else:
        st.warning("No se encontraron datos en Agrocomercial. ⚠️")
        
    