from bs4 import BeautifulSoup
import requests
import re
from .utils import generar_nombre_producto

def extract_ariztia(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'ariztia'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        info_producto = soup.find_all('div', class_='product-item-details')
        
        palabras_claves = [
            'pechuga deshuesada','posta rosada','posta negra','pollo ganso','plateada','lomo vetado',
            'lomo liso','huachalomo','hamburguesa','ganso','carpaccio','molida','carne en tiras',
            'desmechada','cubos','wagyu','huachalomo','abastero','tapapecho','anticuchos','flat iron',
            'marinado','punta paleta','sobrecostilla','asiento','abastero','higado','tártaro','posta paleta',
            'pernil pierna','ala','pernil mano','pollo entero','trutro 1/4','pechuga entera','costillar',
            'pechuga','trutro entero','chuleta centro','chuleta vetada','pulpa ','lomito ','alitas ',
            'longaniza','butifarra ','cerdo en tiras','agrobox','suprema','pana','patas','garras','trutro cuarto',
            'gallina entera','trutro largo','contre ','trutro corto','corazones','nuggets','midwings','trutro',
            'corazón','filetillo','chuleta de centro','pavo entero','apanado','midlegs','lomo centro','trutro',
            'churrasco','asado carnicero','choclillo ','punta picana','entraña','filete','croqueta'
            ]

        for producto in info_producto:
            
            nombre = producto.find('a',class_='product-item-link').text.strip()
            
            nombre_lower = nombre.lower()
            
            etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
            
            p = re.compile(r'\$(\d+\.\d+)\s*(kg)')
            
            precio_kg = producto.find('span', class_='precio-kilo').text
            precio_kg_f = p.search(precio_kg)
            if precio_kg_f:
                numero = precio_kg_f.group(1)
                numero_limpio = numero.replace('.','')
            else:
                numero_limpio = 0
                
            p_ = re.compile(r'\$(\d+\.\d+)\s*')
                
            precio = producto.find('span', class_='price').text
            precio_p = p_.search(precio)
            if precio_p:
                numero_f = precio_p.group(1)
                numero_limpio_f = numero_f.replace('.','')
            else:
                numero_limpio_f = 0
                
            precio_x_kg = int(numero_limpio)
            precio_pagina = int(numero_limpio_f)
            corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)

            try:      
                if nombre != 'sin data':
                    data.append([nombre_tienda,categoria,corte,nombre,precio_x_kg,precio_pagina])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
                    
        print(f"Datos extraídos de Ariztía: {url}")
    else:
        print(f"Error al acceder a Ariztía {url}. Código: {response.status_code}")

    return data


