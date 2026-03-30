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

def extract_frigorificocarnespremium(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'frigorifico premium'
    
    palabras_claves = [
            'pechuga','chuleta centro','huachalomo','posta rosada','chuleta vetada','punta de ganso','tapabarriga','lomo centro','lomo vetado','pierna','pulpa paleta',
            'longaniza','malaya','osobuco','molida','higados','brazuelo','conejo trazado','abastero','choclillo','porterhouse','malaya','costillar','lomo liso','pollo ganso',
            'cordero trozado','asado carnicero','pollo barriga','poncho','costeleta vetada','posta paleta','posta negra','fried rabit','conejo entero',
            'garron delantero','entrecot','asiento','clavo','punta paleta','punta picana','paleta','filete','arrachera','plateada','tapapecho',
            'garron trasero','sobrecostilla','palanca','asado de tira','entraña','flat iron','tomahawk','estomaguillo','cordero entero','ganso','lomo','bife'
            ]
    
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
                    
                    nombre_largo = nombre.lower()
                    precio_neto_kg = precio_limpio
                    precio_neto_total = precio_limpio         
                    
                    nombre_lower = nombre.lower()
        
                    etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
            
                    corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)
                    
                    data.append([
                        nombre_tienda,
                        categoria,
                        corte,
                        nombre_largo, 
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



