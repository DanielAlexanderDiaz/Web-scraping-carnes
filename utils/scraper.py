import streamlit as st
import pandas as pd
import time

def procesar_tienda(nombre_tienda, urls_dict, base_url, extract_function, columns):
    """
    Función genérica para procesar el scraping de cualquier tienda.
    """
    
    urls_items = list(urls_dict.items())  # Lista de tuplas (url, categoria)
    total_urls = len(urls_items)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    timer_text = st.empty()
    
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
        
        # Actualizar progreso y tiempo
        progress = (i + 1) / total_urls
        progress_bar.progress(progress)
        
        elapsed = time.time() - start_time
        mins, secs = divmod(int(elapsed), 60)
        time_str = f"{mins:02d}:{secs:02d}"
        
        status_text.text(f"🔄 {nombre_tienda}: ({i + 1}/{total_urls})")
        timer_text.text(f"⏱️ {time_str} | ETA: {estimate_eta(elapsed, i + 1, total_urls)}")
    
    # Finalización
    status_text.success(f"✅ {nombre_tienda} completado")
    timer_text.text(f"⏱️ Tiempo total: {time_str}")
    progress_bar.progress(1.0)
    time.sleep(0.5)
    
    # Crear DataFrame
    if all_data:
        return pd.DataFrame(all_data, columns=columns)
    return None

def estimate_eta(elapsed_time, completed, total):
    """Calcula el tiempo estimado restante (ETA)"""
    if completed == 0:
        return "calculando..."
    avg_per_url = elapsed_time / completed
    remaining = (total - completed) * avg_per_url
    mins, secs = divmod(int(remaining), 60)
    return f"~{mins:02d}:{secs:02d} restantes"
