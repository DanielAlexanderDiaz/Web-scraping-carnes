import streamlit as st
import pandas as pd
import time
from config import CONFIG_TIENDAS
from scrapers import extract_agrocomercial, extract_ariztia
from utils.scraper import procesar_tienda, estimate_eta

# Lista para acumular todos los DataFrames
dfs_combinados = []

# Procesar cada tienda configurada
for nombre, config in CONFIG_TIENDAS.items():
    st.subheader(f"🛒 Procesando: {nombre.title()}")
    
    df_result = procesar_tienda(
        nombre_tienda=nombre,
        urls_dict=config['urls'],
        base_url=config['base_url'],
        extract_function=config['extractor'],
        columns=config['columns']
    )
    
    if df_result is not None:
        dfs_combinados.append(df_result)
        st.success(f"✅ {len(df_result)} productos extraídos de {nombre}")
    else:
        st.warning(f"⚠️ No se obtuvieron datos de {nombre}")
    
    st.divider()  # Línea separadora visual entre tiendas

# ================================
# COMBINAR TODOS LOS DATAFRAMES
# ================================
if dfs_combinados:
    df_final = pd.concat(dfs_combinados, ignore_index=True)
    
    st.dataframe(
        df_final,
        use_container_width=True
    )
    st.success(f"🎉 Total: {len(df_final)} productos combinados de todas las tiendas")
else:
    st.error("❌ No se pudieron extraer datos de ninguna tienda")

# st.set_page_config(
#     page_title="🥩 Comparador de Precios - Carnes",
#     page_icon="🥩",
#     layout="wide"
# )

# st.title("🥩 Comparador de Precios de Carnes")
# st.markdown("Extrayendo datos de múltiples tiendas...")

# # Sidebar con controles opcionales
# with st.sidebar:
#     st.header("⚙️ Configuración")
#     auto_scrape = st.checkbox("Iniciar scraping automáticamente", value=True)
#     if st.button("🔄 Reiniciar scraping"):
#         st.cache_data.clear()
#         st.rerun()

# # Ejecutar scraping solo si el usuario lo autoriza
# if auto_scrape:
#     # Lista para acumular todos los DataFrames
#     dfs_combinados = []
    
#     # Procesar cada tienda configurada
#     for nombre, config in CONFIG_TIENDAS.items():
#         with st.expander(f"🛒 {nombre.title()}", expanded=True):
#             df_result = procesar_tienda(
#                 nombre_tienda=nombre,
#                 urls_dict=config['urls'],
#                 base_url=config['base_url'],
#                 extract_function=config['extractor'],
#                 columns=config['columns']
#             )
            
#             if df_result is not None:
#                 dfs_combinados.append(df_result)
#                 st.success(f"✅ {len(df_result)} productos extraídos de {nombre}")
#             else:
#                 st.warning(f"⚠️ No se obtuvieron datos de {nombre}")
        
#         st.divider()
    
#     # ================================
#     # COMBINAR TODOS LOS DATAFRAMES
#     # ================================
#     if dfs_combinados:
#         df_final = pd.concat(dfs_combinados, ignore_index=True)
        
#         # 🔥 GUARDAR EN SESSION STATE para usar en filtros/gráficos después
#         st.session_state.df_completo = df_final
#         st.session_state.df_filtro = df_final.copy()  # Para filtros posteriores
        
#         st.success(f"🎉 Total: {len(df_final)} productos combinados de todas las tiendas")
#     else:
#         st.error("❌ No se pudieron extraer datos de ninguna tienda")
# else:
#     st.info("👈 Presiona el checkbox en la barra lateral para iniciar el scraping")

# # ============================================
# # 6️⃣ MOSTRAR RESULTADOS (DESPUÉS del scraping)
# # ============================================
# if 'df_completo' in st.session_state and st.session_state.df_completo is not None:
#     st.subheader("📊 Resultados")
    
#     # Aquí van tus filtros, gráficos y tabla que ya tenías
#     # Ejemplo mínimo:
#     df_display = st.session_state.df_filtro
    
#     # Filtros en sidebar
#     with st.sidebar:
#         st.header("🔍 Filtros")
#         tiendas_disponibles = df_display['Tienda'].unique().tolist()
#         filtro_tienda = st.multiselect("Tienda", tiendas_disponibles)
#         if filtro_tienda:
#             df_display = df_display[df_display['Tienda'].isin(filtro_tienda)]
    
#     # Tabla principal
#     st.dataframe(
#         df_display.sort_values('Precio x KG(neto)', ascending=True),
#         width='stretch',
#         hide_index=True
#     )

# # ============================================
# # 7️⃣ FOOTER
# # ============================================
# st.markdown("---")
# st.caption("🥩 Comparador de Precios de Carnes | Desarrollado por Daniel Díaz")