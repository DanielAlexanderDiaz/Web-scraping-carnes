import re

def generar_nombre_producto(nombre_original, etiqueta_encontrada):
    
    if not etiqueta_encontrada:
        return re.sub(r'\s+', ' ', nombre_original).strip().title()
    
    principal = etiqueta_encontrada[0].title()
    
    nombre_final = f'{principal}'
    
    return nombre_final