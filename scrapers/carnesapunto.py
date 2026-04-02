from bs4 import BeautifulSoup
import requests
import re
from .utils import generar_nombre_producto

def extract_carnesapunto(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'carnes Apunto'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
    
        info_producto = soup.find('div', class_='title-description')
        
        if info_producto:
            
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
            'churrasco','asado carnicero','choclillo ','punta picana','entraña','filete','croqueta','milanesa',
            'pollo ahumado','filetito','panita ','chuletas francesas ','pierna','chuleta parrillera','criadillas',
            'baby back ribs','pulled pork','pata','riñon','chunchules','ubres','lengua','molleja','cola',
            'arrachera','asado de tira','estomaguillo','entrecot','tomahawk','hígado','osobuco','hueso'
            ]

            nombre = info_producto.find('span', class_='product-model').text
            
            
            try:
                texto_corregido = nombre.encode('latin-1').decode('utf-8')
            except Exception as e:
                texto_corregido = nombre
            
            precio = info_producto.find('span',class_='bootic-price').text
            match = re.search(r'\$(\d+\.*\d+)',precio)
            if match:
                precio = match.group(1).replace('.', '')
                precio = int(precio)
            else:
                precio = 0

            div_descripcion = info_producto.find('div', class_='product-description')
            if div_descripcion:     
                pattern = r'\$[\d.]+'
                ff = re.search(pattern, div_descripcion.text)
                if ff:
                    precio_texto = ff.group().replace('$', '').replace('.', '')
                else:
                    precio_texto = 0 
            else:
                precio_texto = 0
                
            nombre_lower = texto_corregido.lower()
            
            etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
                
            corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)
            nombre_largo = texto_corregido
            precio_neto_kg = precio_texto
            precio_neto_total = precio
        
            try:
                if nombre:
                    data.append([nombre_tienda,categoria,corte,nombre_largo,precio_neto_kg,precio_neto_total])
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre_largo} - {e}")
            
    
        print(f'Datos extraidos de {url}')
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")
        
    return data