from bs4 import BeautifulSoup
import requests
import re

def extract_carnes_apunto(url, categoria='sin categoria'):
    response = requests.get(url)
    data = []
    nombre_tienda = 'carnes Apunto'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        nombre = soup.find('span', class_='product-model').text
        precio = soup.find('span',class_='bootic-price').text
        match = re.search(r'\$(\d+\.*\d+)',precio)
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

        data.append([nombre_tienda, categoria, nombre_largo, nombre_corto, nombre_simple, precio_neto_kg, precio_neto_total, precio_bruto_kg, precio_bruto_total])
        # print(f'{nombre_tienda},{categoria},{nombre_largo},{nombre_corto},{nombre_simple},{precio_neto_kg},{precio_neto_total},{precio_bruto_kg},{precio_bruto_total}')
        print(f'Datos extraidos de {url}')
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")
        
    return data

# url_carnes_apunto = {
#         'filete-bife':'vacuno','lomo-liso-c-hueso-chuleton-a-punto':'vacuno','entrecot-a-punto':'vacuno','box-edition-lomo-liso-bife':'vacuno','box-edition-medallon-de-filete':'vacuno',
#         'box-edition-tomahawk':'vacuno','box-edition-lomo-vetado-bife':'vacuno','hamburguesa-chuck-roll':'vacuno','hamburguesa-brisket':'vacuno','mollejas-a-punto':'vacuno',
#         'chunchules':'vacuno','lengua-a-punto':'vacuno','criadillas-de-vacuno':'vacuno','panita-de-vacuno':'vacuno','ubres-de-vacuno-a-punto':'vacuno','rinones':'vacuno',
#         'churrasco-a-punto-2':'vacuno','hueso-tuetano-a-punto':'vacuno','rabo-cola-de-vacuno':'vacuno','asado-de-tira-criollito-a-punto-2':'vacuno','posta-negra-a-punto-congelado':'vacuno',
#         'corazon-de-vacuno-a-punto':'vacuno','pata-de-vacuno-a-punto':'vacuno','estomaguillo':'vacuno','asado-de-tira-criollo-a-punto':'vacuno','tartaro-a-punto':'vacuno',
#         'french-rack-de-tomahawk-2':'vacuno','garron-de-osobuco-prime-1-5-kg':'vacuno','punta-de-ganso-a-punto':'vacuno','lomo-vetado-entero':'vacuno','lomo-vetado-porcionado-a-punto':'vacuno',
#         'lomo-liso-porcionado-a-punto':'vacuno','lomo-vetado-mi-bife':'vacuno','filete-a-punto':'vacuno','punta-picana-a-punto':'vacuno','punta-paleta-flat-iron-a-punto':'vacuno',
#         'plateada-a-punto':'vacuno','asiento-a-punto':'vacuno','liso-bife-350-grs-a-punto':'vacuno','filete-importado-ft':'vacuno','arrachera-1-kg-aprox':'vacuno',
#         'pollo-ganso-a-punto':'vacuno','lomo-liso-a-punto':'vacuno','churrasco-fundo-sur-120-grs':'vacuno',
#         'baby-back-ribs-curacaribs':'cerdo','pulled-pork':'cerdo','baby-back-ribs-campo-noble':'cerdo','costillar-de-cerdo-campo-noble':'cerdo','malaya-de-cerdo':'cerdo',
#         'trutro-corto-granja-magdalena':'pollo','trutro-largo-granja-magdalena':'pollo','pechuga-deshuesada-800grs-granja-magdalena':'pollo','milanesa-de-pollo-familiar-1-kg':'pollo',
#         'pollo-ahumado':'pollo','filetito-de-pollo-800grs-granja-magdalena':'pollo','panita-de-pollo-500-grs-aprox':'pollo','uprema-de-pollo-familiar-in-bocca':'pollo','pollo-entero-1-8-kg-aprox':'pollo',
#         'chuletas-francesas-de-cordero-simunovic':'cordero','pierna-de-cordero-simunovic':'cordero','chuleta-parrillera-de-cordero-simunovic-2':'cordero','criadillas-de-cordero':'cordero',
#     }

# urls_apunto = list(url_carnes_apunto.keys())
# total_urls = len(urls_apunto)
    
# base_apunto = 'https://tienda.carnesapunto.cl/products/'
# all_agro_data = []

# for i, url in enumerate(urls_apunto):
#     clean_url = f"{base_apunto}{url.strip()}"
#     categoria = url_carnes_apunto.get(url, 'sin categoria')
#     try:
#         all_agro_data.extend(extract_carnes_apunto(clean_url, categoria))
#     except Exception as e:
#         print(f"Error en agrocomercial {clean_url}: {e}")
        
# print(all_agro_data)