"""
Módulo de scrapers para comparación de precios de carnes.
Contiene extractores para diferentes tiendas online.
"""

# ============================================
# IMPORTACIONES PÚBLICAS (API del módulo)
# ============================================
from .agrocomercial import extract_agrocomercial
from .ariztia import extract_ariztia
from .carnesapunto import extract_carnesapunto
from .carnesnubles import extract_carnesnubles
from .donacarne import extract_donacarne
from .elcarnicero import extract_elcarnicero
from .frigorifico import extract_frigorifico
from .procarne import extract_procarne

# Opcional: exponer la función compartida si la usas externamente
# from .utils import generar_nombre_producto

# ============================================
# CONTROL DE EXPORTACIÓN CON 'from scrapers import *'
# ============================================
__all__ = [
    'extract_agrocomercial',
    'extract_ariztia',
    'extract_carnesapunto',
    'extract_carnesnubles',
    'extract_donacarne',
    'extract_elcarnicero',
    'extract_frigorifico',
    'extract_procarne'
]

# ============================================
# METADATOS DEL MÓDULO (opcional pero útil)
# ============================================
__version__ = '1.0.0'
__author__ = 'Daniel Díaz'

# ============================================
# FUNCIÓN DE REGISTRO/DEBUG (opcional)
# ============================================
def listar_scrapers_disponibles():
    """
    Retorna una lista con los nombres de los scrapers disponibles.
    Útil para debugging o para generar interfaces dinámicas.
    """
    return [name for name in __all__ if name.startswith('extract_')]