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

def extract_donacarne(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'dona carne'
    
    palabras_claves = [
            'posta rosada','gatorade','sofrito','sal','trutro entero','queso','asiento','trutro 1/4','posta paleta','posta negra','prietas',
            'ensalada','butifarra','arverjas','lomo liso','trutro largo','poroto','choclo','habas ','carbón','filete','papas','longaniza',
            'hueso','pechuga deshuesada','hígado','pechuga entera','paleta centro','costillar','chorizo','molleja','trutro ala','pechuga',
            'pulpa pierna','lomo centro','lomo vetado','molida','coludas','aletilla','entrecott','parrillada','churrasco','tapabarriga',
            'flat iron','tomahawk','pack'
            ]

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
            precio_neto_kg = precio 
            precio_neto_total = precio
            
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

            print(f"Datos extraidos de {url}")
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")

    return data
