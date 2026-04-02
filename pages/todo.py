import streamlit as st
import pandas as pd
from datetime import datetime 
import time
from config import CONFIG_TIENDAS
from utils.scraper import procesar_tienda, contar_total_urls

st.set_page_config(page_title="Carnes CL", layout="wide", page_icon="🥩")

fecha = datetime.now()
st.title(f"Precios de carnes {fecha:%d/%m/%Y}")
st.text("En esta pagina se extraen los precios de carnes de distintos sitios web en Chile 'Agrocomercial, Ariztía, Carnes Apunto, Carnes Bilbao, Carnes Ñubles, Doña carne, El Carnicero, Frigorífico Carnes Premium, Procarne'")

state = st.session_state

if 'categoria' not in state:
    state.categoria = []
if 'nombre' not in state:
    state.nombre = ''  
if 'tienda' not in state:
    state.tienda = []
if 'corte' not in state:
    state.corte = ''
if 'df_filtro' not in state:
    state.df_filtro = None
    

with st.expander("Filtros"):
    filtros = st.container(
        horizontal=True,
        gap="small",
        vertical_alignment="bottom"
    )

    with filtros:
        
            nombre = st.text_input("Nombre del producto", value=state.nombre)
            if nombre!=state.nombre:
                state.nombre = nombre   
                
            categoria = st.multiselect("Categorias", ['vacuno', 'pollo', 'cerdo', 'cordero', 'pavo','otros']) 
            if categoria!=state.categoria:
                state.categoria = categoria
                
            corte = st.text_input("Corte", value=state.corte)
            if corte!=state.corte:
                state.corte = corte
                
            tienda = st.multiselect("Tiendas", ['agrocomercial','ariztia','carnes Apunto','carnes nubles','dona carne', 'el carnicero','frigorifico premium','procarne'])
            if tienda!=state.tienda:
                state.tienda = tienda    
                
            if st.button("Limpiar filtros"):
                state.categoria = []
                state.nombre = ''
                state.tienda = []
                state.corte = ''
                state.df_filtro = None 
    
with st.container():
    if st.button("Iniciar", icon="▶"):
            
        # === BARRA DE PROGRESO GLOBAL ===
        total_global = contar_total_urls(CONFIG_TIENDAS)
        global_progress = st.progress(0)
        global_counter = [0]  # Lista mutable para pasar por referencia
                
        # Lista para acumular todos los DataFrames
        dfs_combinados = []

        progress_container = st.empty()
            
        # Procesar cada tienda configurada
        for nombre, config in CONFIG_TIENDAS.items():
            with progress_container.container():
                st.caption(f"Procesando: {nombre.title()}")
                    
                df_result = procesar_tienda(
                    nombre_tienda=nombre,
                    urls_dict=config['urls'],
                    base_url=config['base_url'],
                    extract_function=config['extractor'],
                    columns=config['columns'],
                    global_progress=global_progress,
                    global_counter=global_counter,
                    global_total=total_global
                )
                    
                if df_result is not None:
                    progress_container.empty()
                    dfs_combinados.append(df_result)
                    # st.success(f"✅ {len(df_result)} productos extraídos de {nombre}")
                else:
                    st.warning(f"⚠️ No se obtuvieron datos de {nombre}")
                    
        progress_container.empty()
                
        # ================================
        # COMBINAR TODOS LOS DATAFRAMES
        # ================================
        if dfs_combinados:
            # Concatenar todos los DataFrames
            df_macro = pd.concat(dfs_combinados, ignore_index=True)
                
            # Eliminar duplicados globales
            df_limpio = df_macro.drop_duplicates(keep='first')
                
            # Convertir columnas numéricas
            columnas_numericas = ['Precio Pagina']
            df_limpio[columnas_numericas] = df_limpio[columnas_numericas].apply(pd.to_numeric, errors='coerce')
                
            # Guardar en la variable única
            state.df_filtro = df_limpio
            
        else:
            st.warning("⚠️ No se encontraron datos en ninguna de las fuentes")
            state.df_filtro = None   
                 
# Estados de los filtros    
if state.df_filtro is not None:
    df = state.df_filtro.copy()
    
    filtro_categoria = state.categoria  
    filtro_nombre = state.nombre.strip()
    filtro_tienda = state.tienda 
    filtro_corte = state.corte
    
    df_display = df 
    
    if filtro_nombre:
        mask_nombre = (
            df['Nombre Pagina'].str.contains(filtro_nombre, case=False, na=False)
        )
        df_display = df_display[mask_nombre]
        
    if filtro_corte:
        mask_corte = (
            df['Corte'].str.contains(filtro_corte, case=False, na=False)
        )
        
        df_display = df_display[mask_corte]
    
    if filtro_categoria and len(filtro_categoria) > 0:
        filtro_categoria_clean = [cat.split(' ', 1)[1] if ' ' in cat else cat for cat in filtro_categoria]
        df_display = df_display[df_display['Categoria'].isin(filtro_categoria_clean)]
        
    if filtro_tienda and len(filtro_tienda) > 0:
        filtro_tienda_clean = [tienda.split(' ', 1)[1] if ' ' in tienda else tienda for tienda in filtro_tienda]
        df_display = df_display[df_display['Tienda'].isin(filtro_tienda_clean)]
        
    # df_display['nuevo precio'] = df_display['precio pagina'] * 1.19
    
    if not df_display.empty:
        
        tab1, tab2 = st.tabs(["📈 Estadisticas", "🔎 Resultados"])
        with tab1:
            st.subheader("🔎 Resultados")
            st.dataframe(
                df_display.sort_values('Precio Pagina', ascending=True),
                width='stretch',
                hide_index=True
            )
            
        with tab2:
            total = len(df_display)
            if total > 0:
                st.write(f'Datos encontrados: {total} ')
                
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("💰 Precio promedio por Categoria")
                precio_por_categoria = df_display.groupby('Categoria')['Precio Pagina'].mean().sort_values(ascending=False)
                st.bar_chart(precio_por_categoria)
            with col2:
                st.subheader("📈 Estadisticas")
            
                st.subheader("💰 Precio promedio por Tienda")
                precio_por_tienda = df_display.groupby('Tienda')['Precio Pagina'].mean().sort_values(ascending=False)
                st.bar_chart(precio_por_tienda)
        
    else:
        st.warning("No se encontraron productos con los filtros seleccionados", icon="⚠️")
        
st.divider()
st.badge("La disponibilidad de los productos depende de la tienda")

st.caption("🥩 Precios de Carnes | Desarrollado por Daniel Díaz")

            

