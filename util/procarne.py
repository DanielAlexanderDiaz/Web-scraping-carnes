from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_procarne(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'procarne'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        nombre = soup.find('h2', class_='h1').text.strip()

        precio = soup.find('span', class_='price-item')         

        if precio is None:
            precio = 0
        else:
            match = re.search(r'\$(\d+\.*\d+)',precio.text.strip())
            if match:
                    precio = match.group(1).replace('.', '')
                    precio = int(precio)

        precio_kg = soup.find('div', class_='pivot-price-per-unit')

        if precio_kg is None:
            precio_kg = 0
        else:
            match = re.search(r'\$(\d+\.*\d+)',precio_kg.text.strip())
            if match:
                    precio_kg = match.group(1).replace('.', '')
                    precio_kg = int(precio_kg)

        nombre_largo = nombre
        nombre_simple = nombre
        precio_neto_kg = precio_kg
        precio_neto_total = precio

        data.append([
            nombre_tienda,
            categoria,
            nombre_largo,
            nombre_simple,
            precio_neto_kg,
            precio_neto_total
            ])
        
        print(f"Datos extraidos de {url}")

    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data
    
