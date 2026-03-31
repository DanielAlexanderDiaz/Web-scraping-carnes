import streamlit as st
import pandas as pd
import time

def estimate_eta(elapsed_time, completed, total):
    """Calcula el tiempo estimado restante (ETA)"""
    if completed == 0:
        return "calculando..."
    avg_per_url = elapsed_time / completed
    remaining = (total - completed) * avg_per_url
    mins, secs = divmod(int(remaining), 60)
    return f"~{mins:02d}:{secs:02d} restantes"

def contar_total_urls(config_tiendas):
    """Calcula el número total de URLs a procesar en todas las tiendas"""
    total = 0
    for config in config_tiendas.values():
        total += len(config['urls'])
    return total

def procesar_tienda(nombre_tienda, urls_dict, base_url, extract_function, columns, global_progress=None, global_counter=None, global_total=None):
    """
    Función genérica para procesar el scraping de cualquier tienda.
    """
    
    urls_items = list(urls_dict.items())  # Lista de tuplas (url, categoria)
    total_urls = len(urls_items)
    
    # Decidir si usar progreso local o global
    if global_progress is None:
        progress_bar = st.progress(0)
        status_text = st.empty()
        timer_text = st.empty()
        usar_progreso_global = False
    else:
        progress_bar = None
        status_text = None
        timer_text = None
        usar_progreso_global = True
        
    all_data = []
    start_time = time.time()
    
    for i, (url, categoria) in enumerate(urls_items):  
        clean_url = f"{base_url}{url.strip()}"
        
        try:
            result = extract_function(clean_url, categoria)
            if result:
                all_data.extend(result)
        except Exception as e:
            print(f"❌ Error en {nombre_tienda} ({clean_url}): {e}")
            st.warning(f"Error procesando {url}", icon="⚠️")
        
        # Actualizar contador global si existe
        if global_counter is not None:
            global_counter[0] += 1

        # Actualizar barra de progreso (global o local)
        if usar_progreso_global and global_progress is not None and global_total is not None:            
            global_progress.progress(min(global_counter[0] / global_total, 1.0))
        elif progress_bar is not None:
            progress_bar.progress((i + 1) / total_urls)
            
        # Actualizar textos solo en modo local
        if not usar_progreso_global:
            elapsed = time.time() - start_time
            mins, secs = divmod(int(elapsed), 60)
            time_str = f"{mins:02d}:{secs:02d}"
            status_text.text(f"🔄 {nombre_tienda}: ({i + 1}/{total_urls})")
            timer_text.text(f"⏱️ {time_str} | ETA: {estimate_eta(elapsed, i + 1, total_urls)}")
    
    # Finalización solo en modo local
    if not usar_progreso_global:
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        status_text.success(f"✅ {nombre_tienda} completado")
        timer_text.text(f"⏱️ Tiempo total: {time_str}")
        progress_bar.progress(1.0)
        time.sleep(0.3)
    
    # Crear DataFrame
    if all_data:
        return pd.DataFrame(all_data, columns=columns)
    return None

