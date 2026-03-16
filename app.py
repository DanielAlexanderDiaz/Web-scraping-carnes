import streamlit as st
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="Precios Competencia", layout="wide")
st.title("Precios Competencia")
st.write("Sitios web donde se extrae la informacion: Agrocomercial, Ariztía, Carnes Apunto, Carnes Bilbao, Carnes Ñubles, Doña carne, El Carnicero, Frigorífico Carnes Premium, Procarne")

# AGROCOMERCIAL
def extract_agrocomercial(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    data = []

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

            try:
                kg_int = float(kg)
                precio_int = int(precio_final)
                valor_kg_total = precio_int / kg_int
                valor_kg_neto = valor_kg_total / 1.19
                valor_kg_neto_int = int(valor_kg_neto)
                nombre_completo = f"{solo_nombre}, {kg} kg"
                if solo_nombre != 'sin data':
                    data.append([nombre_completo, valor_kg_neto_int])
            except (ValueError, ZeroDivisionError) as e:
                print(f"Error procesando producto: {nombre} - {e}")
                continue

        print(f'Datos extraídos de Agrocomercial: {url}')
    else:
        print(f"Error al acceder a Agrocomercial {url}. Código: {response.status_code}")

    return data

# ARIZTIA
def extract_ariztia(url):
    response = requests.get(url)
    data = []

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

            precio_neto = int(valor_numerico / 1.19)

            data.append([nombre, precio_neto, unidad])
        print(f"Datos extraídos de Ariztía: {url}")
    else:
        print(f"Error al acceder a Ariztía {url}. Código: {response.status_code}")

    return data

# CARNES APUNTO
def extract_carnes_apunto(url):
    response = requests.get(url)
    data = []

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
                    

        data.append([nombre, precio, precio_kg])
        # print(f'{nombre},{precio},{precio_kg}')
        print(f'Datos extraidos de {url}')
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")
        
    return data

# CARNES BILBAO
def extract_carnes_bilbao(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('li', class_='product')

        for producto in productos:
            nombre_tag = producto.find('h2', class_='woocommerce-loop-product__title')
            if not nombre_tag:
                continue
            nombre = nombre_tag.get_text(strip=True)

            precio_tag = producto.find('span', class_='woocommerce-Price-amount amount')
            if not precio_tag:
                print(f"Producto sin precio: {nombre}")
                continue  # Saltar si no hay precio

            texto_precio = precio_tag.get_text(strip=True)
            # Eliminar símbolo $ y separadores de miles (.)
            precio_limpio = texto_precio.replace('$', '').replace('.', '')
            
            try:
                valor_numerico = int(precio_limpio)
            except ValueError:
                print(f"Formato de precio inválido en: {nombre} → '{texto_precio}'")
                continue

            data.append([nombre, valor_numerico])
            print(f"Datos extraídos de {url}: {nombre} - ${valor_numerico}")

    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")

    return data

# CARNES ÑUBLES
def extract_carnes_nubles(url):
    response = requests.get(url)
    data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        produtos = soup.find_all('div', class_='yv-product-information')

        for producto in produtos:
            nombre = producto.find('a', class_='yv-product-title').text
            nombre_new = nombre.split("(", 1)[0].strip()

            precio = producto.find('span', class_='yv-product-price').text

            precio_ = re.search(r'\$(\d+\.*\d+)', precio)
            if precio_:
                precio_new = precio_.group(1).replace('.','')
                precio_final = int(precio_new)

            precio_kg = 0
            precio_new_kg = 0
            match = re.search(r'\$(\d+\.\d+|\d+)', nombre)
            if match:
                precio_kg = match.group(1).replace('.','')
                precio_new_kg = int(precio_kg)

            # print(nombre_new,precio_new,precio_kg)
            data.append((nombre_new, precio_final, precio_new_kg))
            print(f"Datos extraidos de {url}")
    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data

# DONACARNE
def extract_donacarne(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        productos = soup.find_all('div', class_='product-border')

        for producto in productos:
            nombre = producto.find('div', class_='product-title').text.strip()
            precio = producto.find('div', class_='product-price').text
            data.append([nombre,precio])
            # print(nombre, precio)
            print(f"Datos extraidos de {url}")
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")

    return data

# ELCARNICERO
def extract_elcarnicero(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        productos = soup.find_all('li', class_='item')

        for producto in productos:
            nombre = producto.find('h2', class_='product-name').text
            precio = producto.find('span', class_='price').text
            data.append([nombre, precio])
            print(f"Datos extraidos de {url}")
    else:
        print(f"Error al acceder a la página {url}. Código de estado: {response.status_code}")

    return data

# FRIGORIFICO CARNES PREMIUM
def extract_frigorificocarnespremium(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        productos = soup.find_all('div', class_='card card--card card--media color-scheme-2 gradient')

        for producto in productos:
            nombre = producto.find('a', class_='full-unstyled-link').text.strip().replace(',', '.')
            precio_tag = producto.find('span', class_='price-item price-item--regular')

            if precio_tag:
                precio_text = precio_tag.text.strip()
                match = re.search(r'\$(\d+\.*\d+)', precio_text)
                if match:
                    precio_limpio = match.group(1).replace('.', '')
                    data.append([nombre, precio_limpio])
                    # print(nombre, precio_limpio)
                else:
                    data.append([nombre, "No encontrado"])
            else:
                data.append([nombre, "Sin precio"])

        print(f"Datos extraídos de {url}")
            
    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data

# PROCARNE
def extract_procarne(url):
    response = requests.get(url)
    data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        nombre = soup.find('h2', class_='h1').text.strip()

        precio = soup.find('span', class_='price-item')         

        if precio is None:
            precio = 0
        else:
            match = re.search(r'\$(\d+\.*\d+)',precio.text.strip())
            if match:
                    precio = match.group(1).replace('.', '')
                    precio = int(precio)

        precio_kg = soup.find('div', class_='pivot-price-per-unit')

        if precio_kg is None:
            precio_kg = 0
        else:
            match = re.search(r'\$(\d+\.*\d+)',precio_kg.text.strip())
            if match:
                    precio_kg = match.group(1).replace('.', '')
                    precio_kg = int(precio_kg)

        # print({nombre},{precio},{precio_kg})
        data.append((nombre,precio,precio_kg))
        print(f"Datos extraidos de {url}")

    else:
        print(f"Error al acceder a {url}: Código {response.status_code}")

    return data

def save_to_excel(agro_data, ariztia_data,carnes_apunto_data,carnes_bilbao_data,carnes_nubles_data,donacarne_data,elcarnicero_data,frigorifico_data,procarne_data):
    output = BytesIO()
    
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        if agro_data:
            df_agro = pd.DataFrame(agro_data, columns=['Producto', 'Precio x kg neto'])
            df_agro.to_excel(writer, sheet_name='Agrocomercial', index=False)
        else:
            print("No hay datos de Agrocomercial para guardar.")

        if ariztia_data:
            df_ariztia = pd.DataFrame(ariztia_data, columns=['Producto', 'neto_x_kg', 'um'])
            df_ariztia.to_excel(writer, sheet_name='Ariztia', index=False)
        else:
            print("No hay datos de Ariztía para guardar.")

        if carnes_apunto_data:
            df_carnes_apunto = pd.DataFrame(carnes_apunto_data, columns=['Producto','Precio','Precio x kg'])
            df_carnes_apunto.to_excel(writer, sheet_name='carnes apunto', index=False)
        else:
            print("No hay datos de carnes apunto para guardar.")
        
        if carnes_bilbao_data:
            df_carnes_bilbao = pd.DataFrame(carnes_bilbao_data, columns=['Producto', 'Precio x kg'])
            df_carnes_bilbao.to_excel(writer, sheet_name='carnes bilbao', index=False)
        else:
            print("No hay datos de carnes bilbao para guardar.")

        if carnes_nubles_data:
            df_carnes_nubles = pd.DataFrame(carnes_nubles_data, columns=['Producto','Precio','Precio x kg'])
            df_carnes_nubles.to_excel(writer, sheet_name='carnes nubles', index=False)
        else:
            print("No hay datos de carnes nubles para guardar.")

        if donacarne_data:
            df_donacarne = pd.DataFrame(donacarne_data, columns=['Producto', 'Precio'])
            df_donacarne.to_excel(writer, sheet_name='doñacarne', index=False)
        else:
            print("No hay datos de doñacarne para guardar.")
        
        if elcarnicero_data:
            df_elcarnicero = pd.DataFrame(elcarnicero_data, columns=['Producto', 'Precio'])
            df_elcarnicero.to_excel(writer, sheet_name='el carnicero', index=False)
        else:
            print("No hay datos de el carnicero para guardar.")
            
        if frigorifico_data:
            df_frigorifico = pd.DataFrame(frigorifico_data, columns=['Producto', 'Precio'])
            df_frigorifico.to_excel(writer, sheet_name='frigorifico premium', index=False)
        else:
            print("No hay datos de el frigorifico para guardar.")
            
        if procarne_data:
            df_procarne = pd.DataFrame(procarne_data, columns=['Producto','Precio','Precio x kg'])
            df_procarne.to_excel(writer, sheet_name='procarne', index=False)
        else:
            print("No hay datos de el procarne para guardar.")
    
    # Obtener los bytes del archivo Excel
    output.seek(0)
    return output.getvalue()

# Botón para iniciar
if st.button("🔍 Extraer datos"):
    # === Contar URLs totales ===
    urls_agro = ['vacuno/','aves/pollo/','cerdo/','cordero/','aves/pavo/','vacuno/elaborados/','detalle/']
    urls_ariztia = [
        'pollo.html','pollo.html?p=2','pollo.html?p=3','pollo.html?p=4','pollo.html?p=5','pollo.html?p=6',
        'pavo.html','pavo.html?p=2','cerdo.html','vacuno.html','vacuno.html?p=2',
        'congelados/hamburguesas.html','congelados/productos-churrasco-lomito-y-bistec.html','congelados/nuggets-y-apanados.html'
    ]
    urls_carnes_apunto = [
        'entrana-a-punto','tapapecho-a-punto','tartaro-a-punto','asiento-a-punto','punta-picana-a-punto','pollo-ganso-a-punto','tomahawk-a-punto','filete-bife','osobuco-a-punto','rabo-cola-de-vacuno',
        'arrachera','filete-a-punto','lomo-vetado-porcionado-a-punto','panita-de-vacuno','lomo-vetado-mi-bife','mollejas-a-punto','guatitas','lomo-liso-porcionado-a-punto','rinones',
        'punta-de-ganso-a-punto','entrecot-a-punto','lomo-liso-a-punto','asado-de-tira-criollo-a-punto','lomo-vetado-entero','punta-paleta-flat-iron-a-punto','posta-negra-a-punto-congelado',
        'plateada-a-punto','lomo-liso-c-hueso-chuleton-a-punto','box-edition-tomahawk','asado-de-tira-criollito-a-punto-2','palanca-a-punto','chunchules','asado-de-tira-ventana',
        'churrasco-a-punto-2','hamburguesa-smoked','criadillas-de-vacuno','hamburguesa-chuck-roll','estomaguillo','french-rack-de-tomahawk-2','hamburguesa-brisket','malaya-de-cerdo',
        'baby-back-ribs-campo-noble','costillar-de-cerdo-campo-noble','baby-back-ribs-curacaribs','pulled-pork','trutro-largo-granja-magdalena','trutro-corto-granja-magdalena','suprema-de-pollo-familiar-in-bocca',
        'pollo-ahumado','chuletas-francesas-de-cordero-simunovic','pierna-de-cordero-simunovic','chuleta-parrillera-de-cordero-simunovic-2','criadillas-de-cordero','butifarra-san-manuelina','longaniza-de-campo-san-manuelina',
        'longanizas-ahumadas-secreto-de-chillan','longanicilla','longaniza-500-gr',
    ]
    urls_carnes_bilbao = [
        'vacuno/','vacuno/page/2/','vacuno/page/3/','vacuno/page/4/','cerdo/','cerdo/page/2/','pollos/',
        'beefeschurrascos/','beefeschurrascos/page/2/','subproductos/','cecinas/','pavos/','hamburguesas/'
    ]
    urls_carnes_nubles = [
        'vacuno','vacuno?page=2&phcursor=eyJhbGciOiJIUzI1NiJ9.eyJzayI6InBvc2l0aW9uIiwic3YiOjM2LCJkIjoiZiIsInVpZCI6NDExMTkwMTc0MDI2NjgsImwiOjM2LCJvIjowLCJyIjoiQ0RQIiwidiI6MSwicCI6Mn0.p7z1Ci39Anp8YX2p1XCHNIHoOgQACAODBlD5YATui7w',
        'cerdo','aves','hamburguesas','churrascos','molidas','apanados','ofertas-flash'
    ]
    urls_donacarne = [
        'vacuno','vacuno?page=2&phcursor=eyJhbGciOiJIUzI1NiJ9.eyJzayI6InBvc2l0aW9uIiwic3YiOjI1LCJkIjoiZiIsInVpZCI6MzE1Mzk0Nzk5MzcxMDUsImwiOjI0LCJvIjowLCJyIjoiQ0RQIiwidiI6MSwicCI6Mn0.c_Hr_E7l3dLxoiEtsB5vgyRGXNsf8hbJTsx0IbeAKfo',
        'vacuno?page=3&phcursor=eyJhbGciOiJIUzI1NiJ9.eyJzayI6InBvc2l0aW9uIiwic3YiOjYyLCJkIjoiZiIsInVpZCI6MzI5MTQ0NzYwNzMwNDEsImwiOjI0LCJvIjowLCJyIjoiQ0RQIiwidiI6MSwicCI6M30.xMnUqFnjDiN7CZC-1tgn0Pqg5wqTDv1xTLQAzcr2wmM','ave','cerdo'
    ]
    urls_elcarnicero = [
        'vacuno.html','cerdo-nacional-o-importado.html','pollo-nacional-o-importado.html','congelados.html',
        'todo-para-el-asado/cortes-para-parrilla.html','todo-para-el-asado/hamburguesas.html','pack.html','ofertas.html','seleccion.html'
    ]
    urls_frigorifico = ['vacuno-1','vacuno-1?page=2','vacuno-1?page=3','cerdo','exoticos','exoticos?page=2']
    urls_procarne = [
        'abastero-angus-origen','arrachera-angus-1','asado-carnicero-angus-origen','asado-de-tira-angus-laminado-congelado-copia','asado-de-tira-angus-copia','asado-de-vacio','asiento-angus-copia','caja-de-hamburguesa-cuarto-libra-114-gr-27-unidades-congelado',
        'choclillo-angus-origen','clavo-parrillero','costeleta-de-lomo-liso-angus-congelado-copia','entrana-angus-origen','entrana-angus','entrecot-angus','estomaguillo-seleccionado-vacio','filete-angus-copia','filete-de-punta-paleta-angus-o-flat-iron-copia','lomo-liso-angus-origen-copia',
        'lomo-vetado-angus-origen-copia','malaya-de-vacuno-origen','osobuco-pierna-trozado-congelado','palanca-angus-copia','plateada-angus-copia','pollo-barriga-angus','pollo-ganso-angus','poncho-parrillero-aranita-angus','posta-negra-angus-origen-copia','posta-rosada',
        'punta-de-ganso-angus','punta-picana-angus-origen-copia','tapabarriga-pieza-seleccionado','tomahawk-angus-origencongelado','costillar-de-cordero','cordero-entero','pierna-de-cordero','chuleta-francesa','paleta-deshuesada-de-cordero','garron-de-pierna-de-cordero',
        'entrecot-de-cordero','chuleta-francesa-mini','cubitos-de-cordero-congelado','garron-de-mano-de-cordero','escalopa-kaiser','carne-cubo','posta-laminada','hamburguesa-225-grs','medallon-de-filete-200-grs','albondigas-100-carne-bolsas-1-kg','bife-aleman',
        'caja-churrascos-500-grs','hamburguesa-all-beef-burger-24-unidades-150-g','caja-de-hamburguesa-cuarto-libra-114-gr-27-unidades-congelado-copia','tomawahk-xl','mini-burger12-estuche-800-grs-con-20-un','albondigas-condimentadas-1kg-congelado',
        'caja-de-hamburguesa-cuarto-libra-114-gr-27-unidades-congelado','caja-de-hamburguesa-casera-de-175-gr-84-unidades-congelado','bocaditos','filetillo-crocante-de-pollo','bistecpechuga','pechuga-entera-de-pollo-deshuesado','filetillo-de-pollo','pechuga-crocante',
        'truto-parrillero','trutro-largo-de-pollo','trutro-corto-de-pollo','pollo-entero','trutro-entero','trutrito-de-ala','hueso-tuetano-de-vacuno','lengua-de-bovino-congelado-copia','criadillas-de-vacuno-origen-congeladas','chunchul-congelado-pieza',
        'mollejas-de-vacuno','rinon-entero-congelado-bandeja',
    ]

    total_urls = (
        len(urls_agro) + len(urls_ariztia) + len(urls_carnes_apunto) + len(urls_carnes_bilbao) +
        len(urls_carnes_nubles) + len(urls_donacarne) + len(urls_elcarnicero) +
        len(urls_frigorifico) + len(urls_procarne)
    )
    # === Inicializar barra de progreso ===
    progress_bar = st.progress(0)
    status_text = st.empty()
    current_step = 0

    # === Agrocomercial ===
    base_agro = 'https://agrocomercial.cl/product-category/'
    all_agro_data = []
    for url in urls_agro:
        clean_url = f"{base_agro}{url.strip()}"
        try:
            all_agro_data.extend(extract_agrocomercial(clean_url))
        except Exception as e:
            print(f"Error en Agrocomercial {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Agrocomercial... ({current_step}/{total_urls})")

    # === Ariztía ===
    base_ariztia = 'https://www.ariztiaatucasa.cl/'
    all_ariztia_data = []
    for url in urls_ariztia:
        clean_url = f"{base_ariztia}{url.strip()}"
        try:
            all_ariztia_data.extend(extract_ariztia(clean_url))
        except Exception as e:
            print(f"Error en Ariztía {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Ariztía... ({current_step}/{total_urls})")

    # === Carnes Apunto ===
    base_apunto = 'https://tienda.carnesapunto.cl/products/'
    all_apunto_data = []
    for url in urls_carnes_apunto:
        clean_url = f"{base_apunto}{url.strip()}"
        try:
            all_apunto_data.extend(extract_carnes_apunto(clean_url))
        except Exception as e:
            print(f"Error en Carnes Apunto {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Carnes Apunto... ({current_step}/{total_urls})")

    # === Carnes Bilbao ===
    base_bilbao = 'https://www.carnesbilbao.cl/categoria-producto/'
    all_bilbao_data = []
    for url in urls_carnes_bilbao:
        clean_url = f"{base_bilbao}{url.strip()}"
        try:
            all_bilbao_data.extend(extract_carnes_bilbao(clean_url))
        except Exception as e:
            print(f"Error en Carnes Bilbao {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Carnes Bilbao... ({current_step}/{total_urls})")

    # === Carnes Ñubles ===
    base_nubles = 'https://carnes.cl/collections/'
    all_nubles_data = []
    for url in urls_carnes_nubles:
        clean_url = f"{base_nubles}{url.strip()}"
        try:
            all_nubles_data.extend(extract_carnes_nubles(clean_url))
        except Exception as e:
            print(f"Error en Carnes Ñubles {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Carnes Ñubles... ({current_step}/{total_urls})")

    # === Doñacarne ===
    base_donacarne = 'https://ventasonline.xn--doacarne-e3a.cl/collections/'
    all_donacarne_data = []
    for url in urls_donacarne:
        clean_url = f"{base_donacarne}{url.strip()}"
        try:
            all_donacarne_data.extend(extract_donacarne(clean_url))
        except Exception as e:
            print(f"Error en Doñacarne {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando doña carne... ({current_step}/{total_urls})")

    # === El Carnicero ===
    base_carnicero = 'https://elcarnicero.cl/'
    all_carnicero_data = []
    for url in urls_elcarnicero:
        clean_url = f"{base_carnicero}{url.strip()}"
        try:
            all_carnicero_data.extend(extract_elcarnicero(clean_url))
        except Exception as e:
            print(f"Error en El Carnicero {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando El Carnicero... ({current_step}/{total_urls})")
    # === Frigorífico Premium ===
    base_frigorifico = 'https://www.frigorificocarnespremium.com/collections/'
    all_frigorifico_data = []
    for url in urls_frigorifico:
        clean_url = f"{base_frigorifico}{url.strip()}"
        try:
            all_frigorifico_data.extend(extract_frigorificocarnespremium(clean_url))
        except Exception as e:
            print(f"Error en Frigorífico {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Frigorífico Premium... ({current_step}/{total_urls})")

    # === Procarne ===
    base_procarne = 'https://www.procarne.cl/products/'
    all_procarne_data = []
    for url in urls_procarne:
        clean_url = f"{base_procarne}{url.strip()}"
        try:
            all_procarne_data.extend(extract_procarne(clean_url))
        except Exception as e:
            print(f"Error en Procarne {clean_url}: {e}")
        current_step += 1
        progress_bar.progress(current_step / total_urls)
        status_text.text(f"Procesando Procarne... ({current_step}/{total_urls})")

    # === Finalizar ===
    status_text.text("✅ Extracción completada.")
    progress_bar.progress(1.0)

    # === Mostrar resultados en tabs ===
    t1,t2,t3,t4,t5,t6,t7,t8,t9 = st.tabs([
        'Agrocomercial', 'Ariztía', 'Carnes Apunto', 'Carnes Bilbao', 'Carnes Ñubles',
        'Donacarne', 'El Carnicero', 'Frigorífico Premium', 'Procarne'
    ])

    with t1: 
        if all_agro_data:
            st.subheader("Agrocomercial.cl")
            df = pd.DataFrame(all_agro_data, columns=['Nombre', 'Precio'])
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Agrocomercial")

    with t2:
        if all_ariztia_data:
            df = pd.DataFrame(all_ariztia_data, columns=['Nombre', 'Precio', 'Unidad'])
            st.subheader("Ariztíaatucasa.cl")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Ariztíaatucasa")

    with t3:
        if all_apunto_data:
            df = pd.DataFrame(all_apunto_data, columns=['Nombre','Precio','Precio x kg'])
            st.subheader("Carnes Apunto")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Carnes Apunto")

    with t4:
        if all_bilbao_data:
            df = pd.DataFrame(all_bilbao_data, columns=['Nombre', 'Precio x kg'])
            st.subheader("Carnes Bilbao")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Carnes Bilbao")

    with t5:
        if all_nubles_data:
            df = pd.DataFrame(all_nubles_data, columns=['Nombre','Precio','Precio x kg'])
            st.subheader("Carnes Ñubles")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Carnes Ñubles")

    with t6:
        if all_donacarne_data:
            df = pd.DataFrame(all_donacarne_data, columns=['Nombre', 'Precio'])
            st.subheader("Doña Carne")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Doña Carne")

    with t7:
        if all_carnicero_data:
            df = pd.DataFrame(all_carnicero_data, columns=['Nombre', 'Precio'])
            st.subheader("El Carnicero")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en El Carnicero")

    with t8:
        if all_frigorifico_data:
            df = pd.DataFrame(all_frigorifico_data, columns=['Nombre', 'Precio'])
            st.subheader("Frigorífico Carnes Premium")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Frigorífico Carnes Premium")

    with t9:
        if all_procarne_data:
            df = pd.DataFrame(all_procarne_data, columns=['Nombre','Precio','Precio x kg'])
            st.subheader("Procarne")
            st.dataframe(df, width='stretch')
        else:
            st.warning("⚠️ No se encontraron datos en Procarne")

    # === Descarga ===
    # excel_bytes = save_to_excel(
    #     all_agro_data, all_ariztia_data, all_apunto_data, all_bilbao_data,
    #     all_nubles_data, all_donacarne_data, all_carnicero_data,
    #     all_frigorifico_data, all_procarne_data
    # )

    # st.download_button(
    #     label="📥 Descargar datos en Excel",
    #     data=excel_bytes,
    #     file_name="precios_carnes.xlsx",
    #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    # )