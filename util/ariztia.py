from bs4 import BeautifulSoup
import requests
import re

def extract_ariztia(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'ariztia'
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('strong', class_='product-item-name')

        for producto in productos:
            link_tag = producto.find('a', class_='product-item-link')
            if not link_tag:
                continue
            nombre_producto = link_tag.text.strip()

            # Limpiar "aprox." y puntos innecesarios
            texto_limpio = re.sub(r'\baprox\.?|\.', '', nombre_producto, flags=re.IGNORECASE).strip()

            # Extraer nombre, cantidad y unidad
            patron_nombre = re.compile(r'^(.*?)\s+(\d+(?:[.,]\d+)?)\s*(kg|gr)\b', re.IGNORECASE)
            match_nombre = patron_nombre.search(texto_limpio)
            if not match_nombre:
                continue

            nombre = match_nombre.group(1).strip()
            cantidad = match_nombre.group(2)
            unidad = match_nombre.group(3).lower()

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

            precio_neto_kg = int(valor_numerico / 1.19)
            
            p = r'(?i)\b(de Pollo|de Vacuno|IQF|Fresco|Congelada|Congelado|2 Un|al vacío|envasado|envasada|Caja de|Granel|granel|Ariztia|Caja|Congeladas|Fresca|de Pavo|porcionada|de Cerdo|al Vacio|envase|Light|.)\b\.?\s*'
            
            nombre_largo = nombre_producto
            nombre_corto = nombre
            nombre_simple = re.sub(p,' ', nombre_corto)
            precio_neto_total = 0 
            precio_bruto_kg = valor_numerico
            precio_bruto_total = 0
            
            try:      
                if nombre_simple != 'sin data':          
                    data.append([
                                nombre_tienda,
                                categoria,
                                nombre_largo.lstrip(), 
                                nombre_corto.lstrip(), 
                                nombre_simple.lstrip(),
                                precio_neto_kg, 
                                precio_neto_total, 
                                precio_bruto_kg, 
                                precio_bruto_total
                                ])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre_largo} - {e}")
                continue
                        
        print(f"Datos extraídos de Ariztía: {url}")
    else:
        print(f"Error al acceder a Ariztía {url}. Código: {response.status_code}")

    return data
