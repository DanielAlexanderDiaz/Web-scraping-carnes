from bs4 import BeautifulSoup
import requests
import re
from math import ceil

def extract_agrocomercial(url, categoria='sin categoria'):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []
    
    nombre_tienda = 'agrocomercial'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('li', class_='status-publish')
        
        for producto in productos:
            solo_nombre = 'sin data'
            kg = 1
            nombre_tag = producto.find('h2', class_='woocommerce-loop-product__title')
            if not nombre_tag:
                continue
            
            nombre = nombre_tag.text.strip()
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
            nombre_corto = f"{solo_nombre}"
            nombre_simple = re.sub(p, ' ', solo_nombre)

            try:    
                if solo_nombre != 'sin data':
                    data.append([
                        nombre_tienda,
                        categoria,
                        nombre_largo, 
                        nombre_corto, 
                        nombre_simple,
                        precio_neto_kg, 
                        precio_neto_total, 
                        precio_bruto_kg, 
                        precio_bruto_total
                        ])   
                        
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue
            
        print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")
    return data





#Codigo de todo.py#

# # ELCARNICERO
# def extract_elcarnicero(url):
#     response = requests.get(url)
#     data = []

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')

#         productos = soup.find_all('li', class_='item')

#         for producto in productos:
#             nombre = producto.find('h2', class_='product-name').text
#             precio = producto.find('span', class_='price').text
#             data.append([nombre, precio])
#             print(f"Datos extraidos de {url}")
#     else:
#         print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")

#     return data
# # FRIGORIFICO CARNES PREMIUM
# def extract_frigorificocarnespremium(url):
#     response = requests.get(url)
#     data = []

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')

#         productos = soup.find_all('div', class_='card card--card card--media color-scheme-2 gradient')

#         for producto in productos:
#             nombre = producto.find('a', class_='full-unstyled-link').text.strip().replace(',', '.')
#             precio_tag = producto.find('span', class_='price-item price-item--regular')

#             if precio_tag:
#                 precio_text = precio_tag.text.strip()
#                 match = re.search(r'\$(\d+\.*\d+)', precio_text)
#                 if match:
#                     precio_limpio = match.group(1).replace('.', '')
#                     data.append([nombre, precio_limpio])
#                     # print(nombre, precio_limpio)
#                 else:
#                     data.append([nombre, "No encontrado"])
#             else:
#                 data.append([nombre, "Sin precio"])

#         print(f"Datos extraídos de {url}")
            
#     else:
#         print(f"Error al acceder a {url}: Código {response.status_code}")

#     return data
# # PROCARNE
# def extract_procarne(url):
#     response = requests.get(url)
#     data = []

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, 'html.parser')

#         nombre = soup.find('h2', class_='h1').text.strip()

#         precio = soup.find('span', class_='price-item')         

#         if precio is None:
#             precio = 0
#         else:
#             match = re.search(r'\$(\d+\.*\d+)',precio.text.strip())
#             if match:
#                     precio = match.group(1).replace('.', '')
#                     precio = int(precio)

#         precio_kg = soup.find('div', class_='pivot-price-per-unit')

#         if precio_kg is None:
#             precio_kg = 0
#         else:
#             match = re.search(r'\$(\d+\.*\d+)',precio_kg.text.strip())
#             if match:
#                     precio_kg = match.group(1).replace('.', '')
#                     precio_kg = int(precio_kg)

#         # print({nombre},{precio},{precio_kg})
#         data.append((nombre,precio,precio_kg))
#         print(f"Datos extraidos de {url}")

#     else:
#         print(f"Error al acceder a {url}: Código {response.status_code}")

#     return data

# # Botón para iniciar
# if st.button("🔍 Extraer datos"):
    # # === Contar URLs totales ===
    # urls_carnes_bilbao = [
    #     'vacuno/','vacuno/page/2/','vacuno/page/3/','vacuno/page/4/','cerdo/','cerdo/page/2/','pollos/',
    #     'beefeschurrascos/','beefeschurrascos/page/2/','subproductos/','cecinas/','pavos/','hamburguesas/'
    # ]
    
    # urls_elcarnicero = [
    #     'vacuno.html','cerdo-nacional-o-importado.html','pollo-nacional-o-importado.html','congelados.html',
    #     'todo-para-el-asado/cortes-para-parrilla.html','todo-para-el-asado/hamburguesas.html','pack.html','ofertas.html','seleccion.html'
    # ]
    # urls_frigorifico = ['vacuno-1','vacuno-1?page=2','vacuno-1?page=3','cerdo','exoticos','exoticos?page=2']
    
    # urls_procarne = [
    #     'abastero-angus-origen','arrachera-angus-1','asado-carnicero-angus-origen','asado-de-tira-angus-laminado-congelado-copia','asado-de-tira-angus-copia','asado-de-vacio','asiento-angus-copia','caja-de-hamburguesa-cuarto-libra-114-gr-27-unidades-congelado',
    #     'choclillo-angus-origen','clavo-parrillero','costeleta-de-lomo-liso-angus-congelado-copia','entrana-angus-origen','entrana-angus','entrecot-angus','estomaguillo-seleccionado-vacio','filete-angus-copia','filete-de-punta-paleta-angus-o-flat-iron-copia','lomo-liso-angus-origen-copia',
    #     'lomo-vetado-angus-origen-copia','malaya-de-vacuno-origen','osobuco-pierna-trozado-congelado','palanca-angus-copia','plateada-angus-copia','pollo-barriga-angus','pollo-ganso-angus','poncho-parrillero-aranita-angus','posta-negra-angus-origen-copia','posta-rosada',
    #     'punta-de-ganso-angus','punta-picana-angus-origen-copia','tapabarriga-pieza-seleccionado','tomahawk-angus-origencongelado','costillar-de-cordero','cordero-entero','pierna-de-cordero','chuleta-francesa','paleta-deshuesada-de-cordero','garron-de-pierna-de-cordero',
    #     'entrecot-de-cordero','chuleta-francesa-mini','cubitos-de-cordero-congelado','garron-de-mano-de-cordero','escalopa-kaiser','carne-cubo','posta-laminada','hamburguesa-225-grs','medallon-de-filete-200-grs','albondigas-100-carne-bolsas-1-kg','bife-aleman',
    #     'caja-churrascos-500-grs','hamburguesa-all-beef-burger-24-unidades-150-g','caja-de-hamburguesa-cuarto-libra-114-gr-27-unidades-congelado-copia','tomawahk-xl','mini-burger12-estuche-800-grs-con-20-un','albondigas-condimentadas-1kg-congelado',
    #     'caja-de-hamburguesa-cuarto-libra-114-gr-27-unidades-congelado','caja-de-hamburguesa-casera-de-175-gr-84-unidades-congelado','bocaditos','filetillo-crocante-de-pollo','bistecpechuga','pechuga-entera-de-pollo-deshuesado','filetillo-de-pollo','pechuga-crocante',
    #     'truto-parrillero','trutro-largo-de-pollo','trutro-corto-de-pollo','pollo-entero','trutro-entero','trutrito-de-ala','hueso-tuetano-de-vacuno','lengua-de-bovino-congelado-copia','criadillas-de-vacuno-origen-congeladas','chunchul-congelado-pieza',
    #     'mollejas-de-vacuno','rinon-entero-congelado-bandeja',
    # ]

    

    # # === Carnes Bilbao ===
    # base_bilbao = 'https://www.carnesbilbao.cl/categoria-producto/'
    # all_bilbao_data = []
    # for url in urls_carnes_bilbao:
    #     clean_url = f"{base_bilbao}{url.strip()}"
    #     try:
    #         all_bilbao_data.extend(extract_carnes_bilbao(clean_url))
    #     except Exception as e:
    #         print(f"Error en Carnes Bilbao {clean_url}: {e}")
    #     current_step += 1
    #     progress_bar.progress(current_step / total_urls)
    #     status_text.text(f"Procesando Carnes Bilbao... ({current_step}/{total_urls})")



    # # === El Carnicero ===
    # base_carnicero = 'https://elcarnicero.cl/'
    # all_carnicero_data = []
    # for url in urls_elcarnicero:
    #     clean_url = f"{base_carnicero}{url.strip()}"
    #     try:
    #         all_carnicero_data.extend(extract_elcarnicero(clean_url))
    #     except Exception as e:
    #         print(f"Error en El Carnicero {clean_url}: {e}")
    #     current_step += 1
    #     progress_bar.progress(current_step / total_urls)
    #     status_text.text(f"Procesando El Carnicero... ({current_step}/{total_urls})")
    # # === Frigorífico Premium ===
    # base_frigorifico = 'https://www.frigorificocarnespremium.com/collections/'
    # all_frigorifico_data = []
    # for url in urls_frigorifico:
    #     clean_url = f"{base_frigorifico}{url.strip()}"
    #     try:
    #         all_frigorifico_data.extend(extract_frigorificocarnespremium(clean_url))
    #     except Exception as e:
    #         print(f"Error en Frigorífico {clean_url}: {e}")
    #     current_step += 1
    #     progress_bar.progress(current_step / total_urls)
    #     status_text.text(f"Procesando Frigorífico Premium... ({current_step}/{total_urls})")

    # # === Procarne ===
    # base_procarne = 'https://www.procarne.cl/products/'
    # all_procarne_data = []
    # for url in urls_procarne:
    #     clean_url = f"{base_procarne}{url.strip()}"
    #     try:
    #         all_procarne_data.extend(extract_procarne(clean_url))
    #     except Exception as e:
    #         print(f"Error en Procarne {clean_url}: {e}")
    #     current_step += 1
    #     progress_bar.progress(current_step / total_urls)
    #     status_text.text(f"Procesando Procarne... ({current_step}/{total_urls})")
