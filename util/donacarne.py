from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_donacarne(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'dona carne'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        productos = soup.find_all('div', class_='product-border')

        for producto in productos:
            nombre = producto.find('div', class_='product-title').text.strip()
            precio = producto.find('div', class_='product-price').text
            
            p = r'\$([\d.]+)'
            
            match = re.search(p, precio)
            if match:
                precio = match.group(1).replace('.', '')
                precio = int(precio)
            else:
                precio = 0
            
            nombre_largo = nombre
            nombre_corto = nombre
            nombre_simple = nombre
            precio_neto_kg = precio 
            precio_neto_total = precio
            precio_bruto_kg = precio
            precio_bruto_total = precio
                        
            data.append([nombre_tienda, categoria, nombre_largo, nombre_corto, nombre_simple, precio_neto_kg, precio_neto_total, precio_bruto_kg, precio_bruto_total])
            print(data)
            print(f"Datos extraidos de {url}")
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")

    return data
