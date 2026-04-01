from bs4 import BeautifulSoup
import requests
import re
# from .utils import generar_nombre_producto

def generar_nombre_producto(nombre_original, etiqueta_encontrada):
    
    if not etiqueta_encontrada:
        return re.sub(r'\s+', ' ', nombre_original).strip().title()
    
    principal = etiqueta_encontrada[0].title()
    
    nombre_final = f'{principal}'
    
    return nombre_final

def extract_ariztia(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'ariztia'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('strong', class_='product-item-name')
        
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

        for producto in productos:
            
            link_tag = producto.find('a', class_='product-item-link')
            if not link_tag:
                continue
            nombre_producto = link_tag.text.strip()
            
            nombre_lower = nombre_producto.lower()
            
            etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]

            # Buscar el precio por kg
            precio_origen = producto.find('span', class_='precio-kilo')
            if not precio_origen:
                continue

            precio_texto = precio_origen.get_text()
            patron_precio = re.compile(r'\$(\d+\.\d+)\s*kg', re.IGNORECASE)
            match_precio = patron_precio.search(precio_texto)
            if not match_precio:
                continue
            
            numero_str = match_precio.group(1)
            valor_limpio = numero_str.replace('.', '')
            valor_numerico = int(valor_limpio)
            
            precio_total_final = 0 
            precio_bruto_kg = int(valor_numerico)    
            nombre_largo = nombre_producto.lstrip()
            corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)

            try:      
                if nombre_largo != 'sin data':
                    data.append([nombre_tienda,categoria,corte,nombre_largo,precio_bruto_kg,precio_total_final])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre_largo} - {e}")
                continue
                    
        print(f"Datos extraídos de Ariztía: {url}")
    else:
        print(f"Error al acceder a Ariztía {url}. Código: {response.status_code}")

    return data


