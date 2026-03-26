from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_carnes_nubles(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        produtos = soup.find_all('div', class_='yv-product-information')

        for producto in produtos:
            nombre = producto.find('a', class_='yv-product-title').text
            nombre_new = nombre.split("(", 1)[0].strip()

            precio = producto.find('span', class_='yv-product-price').text

            precio_ = re.search(r'\$(\d+\.*\d+)', precio)
            if precio_:
                precio_new = precio_.group(1).replace('.','')
                precio_final = int(precio_new)

            precio_kg = 0
            precio_new_kg = 0
            match = re.search(r'\$(\d+\.\d+|\d+)', nombre)
            if match:
                precio_kg = match.group(1).replace('.','')
                precio_new_kg = int(precio_kg)            
            
            nombre_tienda = 'carnes nubles'
            nombre_largo = nombre 
            nombre_corto = nombre_new 
            nombre_simple = nombre_new
            precio_neto_kg = precio_final 
            precio_neto_total = precio_new_kg 
            precio_bruto_kg = 0 
            precio_bruto_total = 0

            data.append((nombre_tienda,categoria,nombre_largo,nombre_corto,nombre_simple,precio_neto_kg,precio_neto_total,precio_bruto_kg,precio_bruto_total))
            
            print(f"Datos extraidos de {url}")
    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data



