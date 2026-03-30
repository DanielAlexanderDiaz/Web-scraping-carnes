from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def generar_nombre_producto(nombre_original, etiqueta_encontrada):
    if not etiqueta_encontrada:
        return re.sub(r'\s+', ' ', nombre_original).strip().title()
    
    principal = etiqueta_encontrada[0].title()
    
    nombre_final = f'{principal}'
    
    return nombre_final

def extract_procarne(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'procarne'
    
    palabras_claves = [
            'trutro de ala','trutro entero','trutro largo','trutro corto','pollo entero','osobuco','pollo ganso','huachalomo','pechuga','poncho','filete',
            'pechuga entera','trutro','estomaguillo','punta paleta','choclillo','sobrecostilla','posta negra','posta rosada','tapabarriga','pollo barriga',
            'asiento','plateada','palanca','arrachera','punta picana','lomo liso','punta de ganso','entrecot','filete','asado de tira','lomo vetado','tomahawk',
            'entraña','asado'
            ]
    
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
                    
        nombre_lower = nombre.lower()
        
        etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
            
        corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)

        nombre_largo = nombre.lower()
        precio_neto_kg = 0
        precio_neto_total = 0

        data.append([
            nombre_tienda,
            categoria,
            corte,
            nombre_largo,
            precio_neto_kg,
            precio_neto_total
            ])
        
        print(f"Datos extraidos de {url}")

    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data
    
