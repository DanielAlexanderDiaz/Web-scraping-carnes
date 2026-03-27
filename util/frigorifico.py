from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_frigorificocarnespremium(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'frigorifico premium'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        productos = soup.find_all('div', class_='card card--card card--media color-scheme-2 gradient')

        for producto in productos:
            nombre = producto.find('a', class_='full-unstyled-link').text.strip().replace(',', '.')
            precio_tag = producto.find('span', class_='price-item price-item--regular')

            if precio_tag:
                precio_text = precio_tag.text.strip()
                match = re.search(r'\$(\d+\.*\d+)', precio_text)
                if match:
                    precio_limpio = match.group(1).replace('.', '')
                    
                    nombre_largo = nombre
                    nombre_simple = nombre
                    precio_neto_kg = precio_limpio
                    precio_neto_total = precio_limpio         
                    
                    data.append([
                        nombre_tienda,
                        categoria,
                        nombre_largo, 
                        nombre_simple,
                        precio_neto_kg,
                        precio_neto_total
                        ])
                else:
                    data.append([nombre, "No encontrado"])
            else:
                data.append([nombre, "Sin precio"])

        print(f"Datos extraídos de {url}")
            
    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data



