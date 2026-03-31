
from bs4 import BeautifulSoup
import requests
import re
from math import ceil
from .utils import generar_nombre_producto

def extract_elcarnicero(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'el carnicero'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        productos = soup.find_all('li', class_='item')
        
        palabras_claves = [
            'filete','lomo liso','posta negra','posta rosada','pollo ganso','ganso','asiento','punta picana','abastero','palanca','huachalomo',
            'sobrecostilla','lomo vetado','tapapecho','posta paleta','punta paleta','choclillo','plateada','asado carnicero','osobuco','aletilla',
            'asado de tira','coluda','hueso','molida','guatacallo','pata','hígado','chunchul','lengua','malaya','tomahawk','mollejas','flat iron',
            'entraña','pulpa pierna','costillar','chuleta centro','chuleta vetada','lomo centro','lomito','pernil mano','cazuela','pulpa','bistec',
            'pechuga deshuesada','pechuga entera','trutro cuarto','trutro ala','trutro largo','trutro entero','pollo entero','filetillo'
            ]
        
        for producto in productos:
            nombre = producto.find('h2', class_='product-name').text
            precio = producto.find('span', class_='price').text
            
            nombre_largo = nombre
            precio_neto_kg = precio
            precio_neto_total = precio
            
            nombre_lower = nombre.lower()
        
            etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
            
            corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)
            
            try:
                if nombre != 'sin data':
                    data.append([
                        nombre_tienda, 
                        categoria,
                        corte,
                        nombre_largo, 
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






    

  