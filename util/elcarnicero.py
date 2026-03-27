
from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_elcarnicero(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'el carnicero'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        productos = soup.find_all('li', class_='item')
        
        for producto in productos:
            nombre = producto.find('h2', class_='product-name').text
            precio = producto.find('span', class_='price').text
            
            nombre_largo = nombre
            nombre_simple = nombre
            precio_neto_kg = precio
            precio_neto_total = precio
            
            try:
                if nombre != 'sin data':
                    data.append([
                        nombre_tienda, 
                        categoria,
                        nombre_largo,
                        nombre_simple, 
                        precio_neto_kg,
                        precio_neto_total
                    ])
            
            except Exception as e:
                print(f"Error al extraer datos del producto: {e}")
                continue
        print(f'Datos extraidos de la página {url}')
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")
    return data






    

  