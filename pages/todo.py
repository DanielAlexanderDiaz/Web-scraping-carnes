import streamlit as st
import pandas as pd
from datetime import datetime 
import util.agrocomercial as agrocomercial
import util.ariztia as ariztia
import util.carnesapunto as carnesapunto
import util.carnesnubles as carnesnubles
import util.donacarne as donacarne
import util.elcarnicero as elcarnicero
import util.frigorifico as frigorifico
import util.procarne as procarne

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
        tienda = st.multiselect("Tiendas", ['agrocomercial','ariztia','carnes Apunto','carnes nubles','dona carne', 'el carnicero','frigorifico premium','procarne'])
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
        df_agro = pd.DataFrame(all_agro_data, columns=['Tienda','Categoria','nombre_largo', 'nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
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
        df_ariz = pd.DataFrame(all_ariz_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
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
        df_apunto = pd.DataFrame(all_apunto_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
        dfs_combinados.append(df_apunto)
        
    # # ======================
    # # PROCESAR CARNES NUBLES
    # # ======================    
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
        df_nubles = pd.DataFrame(all_nubles_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
        dfs_combinados.append(df_nubles)
        
    # # ======================
    # # PROCESAR DOÑA CARNE
    # # ======================  
    url_donacarne = {
    'vacuno':'vacuno',
    'vacuno?page=2':'vacuno',
    'vacuno?page=3':'vacuno',
    'vacuno?page=4':'vacuno',
    'vacuno?page=5':'vacuno',
    'ave':'pollo',
    'ave?page=2':'pollo',
    'cerdo':'cerdo',
    'cerdo?page=2':'cerdo',
    'miscelaneos':'otros',
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
        
    urls_donacarne = list(url_donacarne.keys())
    total_urls = len(urls_donacarne)

    base_donacarne = 'https://ventasonline.xn--doacarne-e3a.cl/collections/'
    all_donacarne_data = []

    for i, url in enumerate(urls_donacarne):
        clean_url = f"{base_donacarne}{url.strip()}"
        categoria = url_donacarne.get(url, 'sin categoria')
        try:
            all_donacarne_data.extend(donacarne.extract_donacarne(clean_url, categoria))
        except Exception as e:
            print(f"Error en dona carne {clean_url}: {e}")
            
    status_text.text(f"Operación completada en dona carne")
    progress_bar.progress(1.0)     
    
    # Procesar DataFrame de dona carne
    if all_donacarne_data:
        df_donacarne = pd.DataFrame(all_donacarne_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
        dfs_combinados.append(df_donacarne)
    
    # # ======================
    # # PROCESAR EL CARNICERO
    # # ======================  
    url_carnicero = {
    'vacuno.html':'vacuno',
    'cerdo-nacional-o-importado.html':'cerdo',
    'pollo-nacional-o-importado.html':'pollo',
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    urls_carnicero = list(url_carnicero.keys())
    total_urls = len(url_carnicero)
        
    base_carnicero = 'https://elcarnicero.cl/'
    all_carnicero_data = []

    for i, url in enumerate(urls_carnicero):
        clean_url = f"{base_carnicero}{url.strip()}"
        categoria = url_carnicero.get(url, 'sin categoria')
        try:
            all_carnicero_data.extend(elcarnicero.extract_elcarnicero(clean_url, categoria))
        except Exception as e:
            print(f"Error en El Carnicero {clean_url}: {e}")
        
    status_text.text(f"Operación completada en el carnicero")
    progress_bar.progress(1.0)       
        
    # Procesar DataFrame de el carnicero
    if all_carnicero_data:
        df_carnicero = pd.DataFrame(all_carnicero_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
        dfs_combinados.append(df_carnicero)
          
    # # ======================
    # # PROCESAR FRIGORIFICO PREMIUM
    # # ======================          
    url_frigorifico = {
    'vacuno-1':'vacuno',
    'vacuno-1?page=2':'vacuno',
    'vacuno-1?page=3':'vacuno',
    'cerdo':'cerdo',
    'exoticos':'cordero',
    'exoticos?page=2':'cordero'
    }

    progress_bar = st.progress(0)
    status_text = st.empty()

    urls_frigorifico = list(url_frigorifico.keys())
    total_urls = len(urls_frigorifico)

    base_frigorifico = 'https://www.frigorificocarnespremium.com/collections/'
    all_frigorifico_data = []
    
    for i, url in enumerate(urls_frigorifico):
        clean_url = f"{base_frigorifico}{url.strip()}"
        categoria = url_frigorifico.get(url, 'sin categoria')
        try:
            all_frigorifico_data.extend(frigorifico.extract_frigorificocarnespremium(clean_url, categoria))
        except Exception as e:
            print(f"Error en Frigorífico {clean_url}: {e}")
      
    status_text.text(f"Operación completada en frigorifico")
    progress_bar.progress(1.0)             
    
    # Procesar DataFrame de frigorifico
    if all_frigorifico_data:
        df_frigorifico = pd.DataFrame(all_frigorifico_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
        dfs_combinados.append(df_frigorifico)
          
    # # ======================
    # # PROCESAR PROCARNE
    # # ====================== 
    url_procarne = {
        'arrachera-angus-1':'vacuno',
        'asado-de-tira-angus-laminado-congelado-copia':'vacuno',
        'asado-de-vacio':'vacuno',
        'asiento-angus-copia':'vacuno',
        'choclillo-angus-origen':'vacuno',
        'costeleta-de-lomo-liso-angus-congelado-copia':'vacuno',
        'costeleta-de-lomo-liso-angus-congelado-copia':'vacuno',
        'entrana-cat-u':'vacuno',
        'entrecot-angus':'vacuno',
        'estomaguillo-seleccionado-vacio':'vacuno',
        'filete-angus-con-cordon':'vacuno',
        'filete-de-punta-paleta-angus-o-flat-iron-copia':'vacuno',
        'filete-u-nacional':'vacuno',
        'huachalomo-angus-copia':'vacuno',
        'lomo-liso-angus-origen-copia':'vacuno',
        'lomo-vetado-angus-origen-copia':'vacuno',
        'osobuco-pierna-trozado-congelado':'vacuno',
        'palanca-angus-copia':'vacuno',
        'plateada-angus-copia':'vacuno',
        'pollo-barriga-angus':'vacuno',
        'pollo-ganso-angus':'vacuno',
        'poncho-parrillero-aranita-angus':'vacuno',
        'posta-negra-angus-origen-copia':'vacuno',
        'posta-rosada':'vacuno',
        'punta-de-ganso-angus':'vacuno',
        'punta-picana-angus-origen-copia':'vacuno',
        'sobrecostilla-seleccionado-pieza':'vacuno',
        'tapabarriga-pieza-seleccionado':'vacuno',
        'tomahawk-angus-origencongelado':'vacuno',
        'bistecpechuga':'pollo',
        'filetillo-crocante-de-pollo':'pollo',
        'pechuga-entera-de-pollo-deshuesado':'pollo',
        'truto-parrillero':'pollo',
        'bocaditos':'pollo',
        'filetillo-de-pollo':'pollo',
        'trutro-corto-de-pollo':'pollo',
        'trutro-largo-de-pollo':'pollo',
        'trutro-entero':'pollo',
        'trutrito-de-ala':'pollo',
        'pechuga-crocante':'pollo',
        'pollo-entero':'pollo',
    }
    
    progress_bar = st.progress(0)
    status_text = st.empty()
        
    urls_procarne = list(url_procarne.keys())
    total_urls = len(urls_procarne)    
    
    base_procarne = 'https://www.procarne.cl/products/'
    all_procarne_data = []
        
    for i, url in enumerate(urls_procarne):
        clean_url = f"{base_procarne}{url.strip()}"
        categoria = url_procarne.get(url, 'sin categoria')
        try:
            all_procarne_data.extend(procarne.extract_procarne(clean_url, categoria))
        except Exception as e:
            print(f"Error en Procarne {clean_url}: {e}")
            
    status_text.text(f"Operación completada en procarne")
    progress_bar.progress(1.0)             
     
    # Procesar DataFrame de procarne
    if all_procarne_data:
        df_procarne = pd.DataFrame(all_procarne_data, columns=['Tienda','Categoria','nombre_largo','nombre_simple', 'precio_neto_kg', 'precio_neto_total'])
        dfs_combinados.append(df_procarne)    
          
    # ========================
    # 3. COMBINAR Y LIMPIAR TODOS LOS DATOS
    # ========================
    if dfs_combinados:
        # Concatenar todos los DataFrames
        df_macro = pd.concat(dfs_combinados, ignore_index=True)
        
        # Eliminar duplicados globales
        df_limpio = df_macro.drop_duplicates(keep='first')
        
        # Convertir columnas numéricas
        columnas_numericas = ['precio_neto_kg', 'precio_neto_total']
        df_limpio[columnas_numericas] = df_limpio[columnas_numericas].apply(pd.to_numeric, errors='coerce')
        
        # Guardar en la variable única
        state.df_filtro = df_limpio
    
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
        
        total = len(df_display)
        if total > 0:
            st.write(total)
            
        st.dataframe(
            df_display.sort_values('precio_neto_kg', ascending=True),
            width='stretch',
            hide_index=True
        )
        
    else:
        st.warning("No se encontraron productos con los filtros seleccionados", icon="⚠️")
        

            

