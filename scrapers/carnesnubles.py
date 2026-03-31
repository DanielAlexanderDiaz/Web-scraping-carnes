from bs4 import BeautifulSoup
import requests
import re
from math import ceil
from .utils import generar_nombre_producto

def extract_carnesnubles(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        produtos = soup.find_all('div', class_='yv-product-information')
        
        palabras_claves = [
            'chuleta de centro','chuleta vetada','panceta','chinchulin','lomito','truto corto','hueso',
            'malaya','tuto alita','pastrami','truto largo','pechuga','teclas de lomo','pollo entero',
            'choclillo','abastero','posta paleta','palanca','lomo vetado','flat iron','entraña','sobrecostilla',
            'tapapecho','entrecot','arrachera','pollo ganso','costeleta','abastero','lengua','costillar','huachalomo',
            'punta picana','posta negra','punta paleta','posta rosada','palanca','poncho','petit tender','clavo','asiento',
            'asado carnicero','pollo barriga','lomo liso','croqueta','tapabarriga','hamburguesa','punta de ganso','tomahawk',
            'lomo liso','filete','plateada','asado de tira'
            ]

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
                
            nombre_lower = nombre.lower()
        
            etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
            
            corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)
            
            nombre_tienda = 'carnes nubles'
            nombre_largo = nombre 
            precio_neto_kg = precio_final 
            precio_neto_total = precio_new_kg 

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



