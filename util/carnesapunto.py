from bs4 import BeautifulSoup
import requests
import re

def generar_nombre_producto(nombre_original, etiqueta_encontrada):
    if not etiqueta_encontrada:
        return re.sub(r'\s+', ' ', nombre_original).strip().title()
    
    principal = etiqueta_encontrada[0].title()
    
    nombre_final = f'{principal}'
    
    return nombre_final

def extract_carnes_apunto(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'carnes Apunto'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        nombre = soup.find('span', class_='product-model').text
        precio = soup.find('span',class_='bootic-price').text
        match = re.search(r'\$(\d+\.*\d+)',precio)
        
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
            'baby back ribs','pulled pork','pata','riñon','chunchules','ubres','lengua','molleja','cola','garron de osobuco',
            'arrachera','asado de tira','estomaguillo','entrecot','tomahawk'
            ]
        
        nombre_lower = nombre.lower()
        
        etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
        
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

        corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)
        
        data.append([
            nombre_tienda, 
            categoria, 
            corte,
            nombre_largo,   
            precio_neto_kg, 
            precio_neto_total
            ])
    
        print(f'Datos extraidos de {url}')
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")
        
    return data