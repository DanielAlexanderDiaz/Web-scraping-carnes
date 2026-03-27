from bs4 import BeautifulSoup
import requests
import re

def extract_carnes_apunto(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'carnes Apunto'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        nombre = soup.find('span', class_='product-model').text
        precio = soup.find('span',class_='bootic-price').text
        match = re.search(r'\$(\d+\.*\d+)',precio)
        if match:
            precio = match.group(1).replace('.', '')
            precio = int(precio)
        else:
            precio = 0

        div_descripcion = soup.find('div', class_='product-description only-description')

        if div_descripcion is None:
            precio_kg = 0
        else:
            texto = div_descripcion.get_text(strip=True)
            numeros = re.findall(r'\d+\.?\d*', texto)
            precio_kg = 0
            for num in numeros:
                if len(num)>3:
                    precio_kg = num
                    match = re.search(r'\$(\d+\.*\d+)',precio_kg)
                    if match:
                        precio_kg = match.group(1).replace('.', '')
                        precio_kg = int(precio_kg)
                    
        nombre_largo = nombre 
        nombre_corto = nombre
        nombre_simple = nombre
        precio_neto_kg = precio_kg
        precio_neto_total = precio
        precio_bruto_kg = precio
        precio_bruto_total = precio

        data.append([
            nombre_tienda, 
            categoria, 
            nombre_largo,  
            nombre_simple, 
            precio_neto_kg, 
            precio_neto_total
            ])
    
        print(f'Datos extraidos de {url}')
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")
        
    return data