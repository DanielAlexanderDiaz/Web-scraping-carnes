import streamlit as st
import pandas as pd
from datetime import datetime 
import util.agrocomercial as agrocomercial
import util.ariztia as ariztia
import util.carnesapunto as carnesapunto
import util.carnesnubles as carnesnubles

st.set_page_config(page_title="Carnes CL", layout="wide", page_icon="🥩")

fecha = datetime.now()
st.title(f"Precios de carnes {fecha:%d/%m/%Y}")
st.text("En esta pagina se extraen los precios de carnes de distintos sitios web en Chile 'Agrocomercial, Ariztía, Carnes Apunto, Carnes Bilbao, Carnes Ñubles, Doña carne, El Carnicero, Frigorífico Carnes Premium, Procarne'")

state = st.session_state

if 'categoria' not in state:
    state.categoria = []
if 'nombre' not in state:
    state.nombre = ""  
if 'tienda' not in state:
    state.tienda = []
if 'df_filtro' not in state:
    state.df_filtro = None
    
#filtro
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        nombre = st.text_input("Nombre del producto", value=state.nombre)
        if nombre!=state.nombre:
            state.nombre = nombre   
    with c2:
        categoria = st.multiselect("Categorias", ['vacuno', 'pollo', 'cerdo', 'cordero', 'pavo','otros']) 
        if categoria!=state.categoria:
            state.categoria = categoria
    with c3:
        tienda = st.multiselect("Tiendas", ['agrocomercial','ariztia','carnes Apunto','carnes nubles'])
        if tienda!=state.tienda:
            state.tienda = tienda
       
#extraer info     
if st.button("Extraer datos"):
    
    # Lista para acumular todos los DataFrames limpios
    dfs_combinados = []
    
    # ======================
    # PROCESAR AGROCOMERCIAL
    # ======================
    url_agro = {
        'vacuno/':'vacuno', 
        'aves/pollo/':'pollo', 
        'cerdo/':'cerdo',
        'cordero/':'cordero', 
        'aves/pavo/':'pavo'
    }
    urls_agro = list(url_agro.keys())
    total_urls = len(urls_agro)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    base_agro = 'https://agrocomercial.cl/product-category/'
    all_agro_data = []
    
    for i, url in enumerate(urls_agro):
        clean_url = f"{base_agro}{url.strip()}"
        categoria = url_agro.get(url, 'sin categoria')
        try:
            all_agro_data.extend(agrocomercial.extract_agrocomercial(clean_url, categoria))
        except Exception as e:
            print(f"Error en agrocomercial {clean_url}: {e}")
        progress_bar.progress((i + 1) / total_urls)
        status_text.text(f"agrocomercial en proceso... ({i + 1}/{total_urls})")
    
    status_text.text(f"Operación completada en agrocomercial")
    progress_bar.progress(1.0)
    
    # Procesar DataFrame de agrocomercial
    if all_agro_data:
        df_agro = pd.DataFrame(all_agro_data, columns=['Tienda','Categoria','nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        dfs_combinados.append(df_agro)
    
    # ================
    # PROCESAR ARIZTIA
    # ================
    url_ariz = {
        'pollo.html':'pollo', 'pollo.html?p=2':'pollo', 'pollo.html?p=3':'pollo','pollo.html?p=4':'pollo', 'pollo.html?p=5':'pollo', 'pollo.html?p=6':'pollo',
        'pavo.html':'pavo', 'pavo.html?p=2':'pavo', 'cerdo.html':'cerdo','vacuno.html':'vacuno', 'vacuno.html?p=2':'vacuno','congelados/hamburguesas.html':'otros',
        'congelados/productos-churrasco-lomito-y-bistec.html':'otros','congelados/nuggets-y-apanados.html':'otros',
    }
    
    urls_ariz = list(url_ariz.keys())
    total_urls = len(urls_ariz)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    base_ariz = 'https://www.ariztiaatucasa.cl/'
    all_ariz_data = []
    
    for i, url in enumerate(urls_ariz):
        clean_url = f"{base_ariz}{url.strip()}"
        categoria = url_ariz.get(url, 'sin categoria')
        try:
            all_ariz_data.extend(ariztia.extract_ariztia(clean_url, categoria))
        except Exception as e:
            print(f"Error en ariztia {clean_url}: {e}")
        progress_bar.progress((i + 1) / total_urls)
        status_text.text(f"ariztia en proceso... ({i + 1}/{total_urls})")
    
    status_text.text(f"Operación completada en ariztia")
    progress_bar.progress(1.0)
    
    # Procesar DataFrame de ariztia
    if all_ariz_data:
        df_ariz = pd.DataFrame(all_ariz_data, columns=['Tienda','Categoria','nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        dfs_combinados.append(df_ariz)
    
    # ======================
    # PROCESAR CARNES APUNTO
    # ======================
    url_carnes_apunto = {
        'filete-bife':'vacuno','lomo-liso-c-hueso-chuleton-a-punto':'vacuno','entrecot-a-punto':'vacuno','box-edition-lomo-liso-bife':'vacuno','box-edition-medallon-de-filete':'vacuno',
        'box-edition-tomahawk':'vacuno','box-edition-lomo-vetado-bife':'vacuno','hamburguesa-chuck-roll':'vacuno','hamburguesa-brisket':'vacuno','mollejas-a-punto':'vacuno',
        'chunchules':'vacuno','lengua-a-punto':'vacuno','criadillas-de-vacuno':'vacuno','panita-de-vacuno':'vacuno','ubres-de-vacuno-a-punto':'vacuno','rinones':'vacuno',
        'churrasco-a-punto-2':'vacuno','hueso-tuetano-a-punto':'vacuno','rabo-cola-de-vacuno':'vacuno','asado-de-tira-criollito-a-punto-2':'vacuno','posta-negra-a-punto-congelado':'vacuno',
        'corazon-de-vacuno-a-punto':'vacuno','pata-de-vacuno-a-punto':'vacuno','estomaguillo':'vacuno','asado-de-tira-criollo-a-punto':'vacuno','tartaro-a-punto':'vacuno',
        'french-rack-de-tomahawk-2':'vacuno','garron-de-osobuco-prime-1-5-kg':'vacuno','punta-de-ganso-a-punto':'vacuno','lomo-vetado-entero':'vacuno','lomo-vetado-porcionado-a-punto':'vacuno',
        'lomo-liso-porcionado-a-punto':'vacuno','lomo-vetado-mi-bife':'vacuno','filete-a-punto':'vacuno','punta-picana-a-punto':'vacuno','punta-paleta-flat-iron-a-punto':'vacuno',
        'plateada-a-punto':'vacuno','asiento-a-punto':'vacuno','liso-bife-350-grs-a-punto':'vacuno','filete-importado-ft':'vacuno','arrachera-1-kg-aprox':'vacuno',
        'pollo-ganso-a-punto':'vacuno','lomo-liso-a-punto':'vacuno','churrasco-fundo-sur-120-grs':'vacuno',
        'baby-back-ribs-curacaribs':'cerdo','pulled-pork':'cerdo','baby-back-ribs-campo-noble':'cerdo','costillar-de-cerdo-campo-noble':'cerdo','malaya-de-cerdo':'cerdo',
        'trutro-corto-granja-magdalena':'pollo','trutro-largo-granja-magdalena':'pollo','pechuga-deshuesada-800grs-granja-magdalena':'pollo','milanesa-de-pollo-familiar-1-kg':'pollo',
        'pollo-ahumado':'pollo','filetito-de-pollo-800grs-granja-magdalena':'pollo','panita-de-pollo-500-grs-aprox':'pollo','uprema-de-pollo-familiar-in-bocca':'pollo','pollo-entero-1-8-kg-aprox':'pollo',
        'chuletas-francesas-de-cordero-simunovic':'cordero','pierna-de-cordero-simunovic':'cordero','chuleta-parrillera-de-cordero-simunovic-2':'cordero','criadillas-de-cordero':'cordero',
    }
    
    urls_apunto = list(url_carnes_apunto.keys())
    total_urls = len(urls_apunto)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    base_apunto = 'https://tienda.carnesapunto.cl/products/'
    all_apunto_data = []

    for i, url in enumerate(urls_apunto):
        clean_url = f"{base_apunto}{url.strip()}"
        categoria = url_carnes_apunto.get(url, 'sin categoria')
        try:
            all_apunto_data.extend(carnesapunto.extract_carnes_apunto(clean_url, categoria))
        except Exception as e:
            print(f"Error en agrocomercial {clean_url}: {e}")
        progress_bar.progress((i + 1) / total_urls)
        status_text.text(f"carnes apunto en proceso... ({i + 1}/{total_urls})")
    
    status_text.text(f"Operación completada en carnes apunto")
    progress_bar.progress(1.0)
    
    # Procesar DataFrame de carne a punto
    if all_apunto_data:
        df_apunto = pd.DataFrame(all_apunto_data, columns=['Tienda','Categoria','nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        dfs_combinados.append(df_apunto)
        
    # ======================
    # PROCESAR CARNES NUBLES
    # ======================    
    url_carnes_nubles = {
    'vacuno':'vacuno',
    'vacuno?page=2':'vacuno',
    'cerdo':'cerdo',
    'aves':'aves',
    }
    
    urls_nubles= list(url_carnes_nubles.keys())
    total_urls = len(urls_nubles)
     
    progress_bar = st.progress(0)
    status_text = st.empty()
           
    base_nubles = 'https://carnes.cl/collections/'
    all_nubles_data = []

    for i, url in enumerate(urls_nubles):
        clean_url = f"{base_nubles}{url.strip()}"
        categoria = url_carnes_nubles.get(url, 'sin categoria')
        try:
            all_nubles_data.extend(carnesnubles.extract_carnes_nubles(clean_url, categoria))
        except Exception as e:
            print(f"Error en Carnes Ñubles {clean_url}: {e}")
            
    status_text.text(f"Operación completada en carnes nubles")
    progress_bar.progress(1.0)     
    
    # Procesar DataFrame de carne nubles
    if all_nubles_data:
        df_nubles = pd.DataFrame(all_nubles_data, columns=['Tienda','Categoria','nombre_largo', 'nombre_corto', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total'])
        dfs_combinados.append(df_nubles)
        
    # ========================
    # 3. COMBINAR Y LIMPIAR TODOS LOS DATOS
    # ========================
    if dfs_combinados:
        # Concatenar todos los DataFrames
        df_macro = pd.concat(dfs_combinados, ignore_index=True)
        
        # Eliminar duplicados globales
        df_limpio = df_macro.drop_duplicates(keep='first')
        
        # Convertir columnas numéricas
        columnas_numericas = ['precio_neto_kg', 'precio_neto_total', 'precio_bruto_kg', 'precio_bruto_total']
        df_limpio[columnas_numericas] = df_limpio[columnas_numericas].apply(pd.to_numeric, errors='coerce')
        
        # Guardar en la variable única
        state.df_filtro = df_limpio
        st.success(f"✅ Datos combinados: {len(df_limpio)} registros extraídos de ambas tiendas")
    else:
        st.warning("⚠️ No se encontraron datos en ninguna de las fuentes")
        state.df_filtro = None        
        
if state.df_filtro is not None:
    df = state.df_filtro.copy()
    
    filtro_categoria = state.categoria  
    filtro_nombre = state.nombre.strip()
    filtro_tienda = state.tienda 
    
    df_display = df 
    
    if filtro_nombre:
        mask_nombre = (
            df['nombre_simple'].str.contains(filtro_nombre, case=False, na=False) |
            df['nombre_corto'].str.contains(filtro_nombre, case=False, na=False) |
            df['nombre_largo'].str.contains(filtro_nombre, case=False, na=False)
        )
        df_display = df_display[mask_nombre]
    
    if filtro_categoria and len(filtro_categoria) > 0:
        df_display = df_display[df_display['Categoria'].isin(filtro_categoria)]
        
    if filtro_tienda and len(filtro_tienda) > 0:
        df_display = df_display[df_display['Tienda'].isin(filtro_tienda)]
    
    if not df_display.empty:
        st.dataframe(
            df_display.sort_values('precio_neto_kg', ascending=True),
            width='stretch',
            hide_index=True
        )
    else:
        st.warning("No se encontraron productos con los filtros seleccionados", icon="⚠️")
        

            

