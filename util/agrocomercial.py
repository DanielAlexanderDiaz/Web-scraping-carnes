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
    

def extract_agrocomercial(url, categoria='sin categoria'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []
    
    nombre_tienda = 'agrocomercial'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('li', class_='status-publish')
        
        palabras_claves = [
            'pechuga deshuesada','posta rosada','posta negra','pollo ganso','plateada','lomo vetado',
            'lomo liso','huachalomo','hamburguesa','ganso','carpaccio','molida','carne en tiras',
            'desmechada','cubos','wagyu','huachalomo','abastero','tapapecho','anticuchos','flat iron',
            'marinado','punta paleta','sobrecostilla','asiento','abastero','higado','tártaro','posta paleta',
            'pernil pierna','ala','pernil mano','pollo entero','trutro 1/4','pechuga entera','costillar',
            'pechuga','trutro entero','chuleta centro','chuleta vetada','pulpa ','lomito ','alitas ',
            'longaniza','butifarra ','cerdo en tiras','agrobox','suprema'
            ]
        
        for producto in productos:
            
            solo_nombre = 'sin data'
            kg = 1
            nombre_tag = producto.find('h2', class_='woocommerce-loop-product__title')
            if not nombre_tag:
                continue
            
            nombre = nombre_tag.text.strip()
            nombre_lower = nombre.lower()
            
            etiquetas_encontradas = [palabra for palabra in palabras_claves if palabra in nombre_lower]
            
            patron_peso = r"(\d+\.?\d*)\s*(kg|g)" 
            peso_encontrado = re.search(patron_peso, nombre, re.IGNORECASE)
    
            patron = r'^(.*?)\s+(\d+(?:\.\d+)?)\s*[kK][gG]\b'
            match = re.match(patron, nombre)
            
            if match:
                solo_nombre = match.group(1).strip()
                kg = match.group(2)

            precio_final = None
            ins_tag = producto.find('ins')
            
            if ins_tag:
                precio_final = ins_tag.get_text(strip=True).replace('$', '').replace('.', '')
            else:
                span_precio = producto.find('span', class_='woocommerce-Price-amount')
                if span_precio:
                    precio_final = span_precio.get_text(strip=True).replace('$', '').replace('.', '')
                else:
                    continue  # Saltar si no hay precio
                
            p = r'(?i)\b(CAT-V|Caja|CONGELADO|Vacio|Porc.|Vacuno|de Vacuno|de Cerdo|Porc|Cat V|de Pollo|Cajas de|Porcionada|Porcionado|2.0 aprox|Congelada|Fresca|.)\b\.?\s*'
                
            kg_int = int(kg)
            precio_bruto_total = int((precio_final))
            precio_bruto_kg = ceil(precio_bruto_total/kg_int)
            precio_neto_total = ceil(precio_bruto_total/1.19)
            precio_neto_kg = ceil(precio_bruto_kg/1.19)
            nombre_largo = f"{solo_nombre}, {kg} kg"
            
            try:    
                if solo_nombre != 'sin data':
                        
                    corte = generar_nombre_producto(nombre_lower, etiquetas_encontradas)
                        
                    data.append([
                        nombre_tienda,
                        categoria,
                        corte,
                        nombre_largo,  
                        precio_neto_kg, 
                        precio_neto_total
                        ])  
                        
                    # print(nombre_tienda,categoria,nombre_largo) 
                    # print(nombre_lower)
                    # print(etiquetas_encontradas)    
                    # print(etiquetas_encontradas, peso_encontrado.group(0))
                    # print(f"Peso detectado: {peso_encontrado.group(0)}") # Salida: 5 kg
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
            
        # print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")
    return data
