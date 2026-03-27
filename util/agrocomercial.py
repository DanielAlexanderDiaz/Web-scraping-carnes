from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_agrocomercial(url, categoria='sin categoria'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []
    
    nombre_tienda = 'agrocomercial'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
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
                
            p = r'(?i)\b(CAT-V|Caja|CONGELADO|Vacio|Porc.|Vacuno|de Vacuno|de Cerdo|Porc|Cat V|de Pollo|Cajas de|Porcionada|Porcionado|2.0 aprox|Congelada|Fresca|.)\b\.?\s*'
                
            kg_int = int(kg)
            precio_bruto_total = int((precio_final))
            precio_bruto_kg = ceil(precio_bruto_total/kg_int)
            precio_neto_total = ceil(precio_bruto_total/1.19)
            precio_neto_kg = ceil(precio_bruto_kg/1.19)
            nombre_largo = f"{solo_nombre}, {kg} kg"
            nombre_corto = f"{solo_nombre}"
            nombre_simple = re.sub(p, ' ', solo_nombre)

            try:    
                if solo_nombre != 'sin data':
                    data.append([
                        nombre_tienda,
                        categoria,
                        nombre_largo,  
                        nombre_simple,
                        precio_neto_kg, 
                        precio_neto_total
                        ])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
            
        print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")
    return data