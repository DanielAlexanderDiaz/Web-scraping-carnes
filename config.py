from scrapers import extract_agrocomercial, extract_ariztia, extract_carnesapunto, extract_carnesnubles, extract_donacarne, extract_elcarnicero, extract_frigorifico, extract_procarne
# ================================
# CONFIGURACIÓN DE TIENDAS
# ================================
CONFIG_TIENDAS = {
    'agrocomercial': {
        'base_url': 'https://agrocomercial.cl/product-category/',
        'urls': {
            'vacuno/': 'vacuno', 
            'aves/pollo/': 'pollo', 
            'cerdo/': 'cerdo',
            'cordero/': 'cordero', 
            'aves/pavo/': 'pavo'
        },
        'extractor': extract_agrocomercial,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'ariztia': {
        'base_url': 'https://www.ariztiaatucasa.cl/',
        'urls': {
            'pollo.html':'pollo', 'pollo.html?p=2':'pollo', 'pollo.html?p=3':'pollo',
            'pollo.html?p=4':'pollo', 'pollo.html?p=5':'pollo', 'pollo.html?p=6':'pollo',
            'pavo.html':'pavo', 'pavo.html?p=2':'pavo', 'cerdo.html':'cerdo',
            'vacuno.html':'vacuno', 'vacuno.html?p=2':'vacuno',
            'congelados/hamburguesas.html':'otros',
            'congelados/productos-churrasco-lomito-y-bistec.html':'otros',
            'congelados/nuggets-y-apanados.html':'otros',
        },
        'extractor': extract_ariztia,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'carnesapunto': {
        'base_url': 'https://tienda.carnesapunto.cl/products/',
        'urls': {
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
        },
        'extractor': extract_carnesapunto,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'carnesnubles': {
        'base_url': 'https://carnes.cl/collections/',
        'urls': {
            'vacuno':'vacuno',
            'vacuno?page=2':'vacuno',
            'cerdo':'cerdo',
            'aves':'pollo',
        },
        'extractor': extract_carnesnubles,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'donacarne': {
        'base_url': 'https://ventasonline.xn--doacarne-e3a.cl/collections/',
        'urls': {
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
        },
        'extractor': extract_donacarne,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'elcarnicero': {
        'base_url': 'https://elcarnicero.cl/',
        'urls': {
            'vacuno.html':'vacuno',
            'cerdo-nacional-o-importado.html':'cerdo',
            'pollo-nacional-o-importado.html':'pollo',
        },
        'extractor': extract_elcarnicero,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'frigorifico': {
        'base_url': 'https://www.frigorificocarnespremium.com/collections/',
        'urls': {
            'vacuno-1':'vacuno',
            'vacuno-1?page=2':'vacuno',
            'vacuno-1?page=3':'vacuno',
            'cerdo':'cerdo',
            'exoticos':'cordero',
            'exoticos?page=2':'cordero'
        },
        'extractor': extract_frigorifico,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
    'procarne': {
        'base_url': 'https://www.procarne.cl/products/',
        'urls': {
            'arrachera-angus-1':'vacuno','asado-de-tira-angus-laminado-congelado-copia':'vacuno','asado-de-vacio':'vacuno','asiento-angus-copia':'vacuno','choclillo-angus-origen':'vacuno',
            'costeleta-de-lomo-liso-angus-congelado-copia':'vacuno','costeleta-de-lomo-liso-angus-congelado-copia':'vacuno','entrana-cat-u':'vacuno','entrecot-angus':'vacuno',
            'estomaguillo-seleccionado-vacio':'vacuno','filete-angus-con-cordon':'vacuno','filete-de-punta-paleta-angus-o-flat-iron-copia':'vacuno','filete-u-nacional':'vacuno',
            'huachalomo-angus-copia':'vacuno','lomo-liso-angus-origen-copia':'vacuno','lomo-vetado-angus-origen-copia':'vacuno','osobuco-pierna-trozado-congelado':'vacuno',
            'palanca-angus-copia':'vacuno','plateada-angus-copia':'vacuno','pollo-barriga-angus':'vacuno','pollo-ganso-angus':'vacuno','poncho-parrillero-aranita-angus':'vacuno','posta-rosada':'vacuno',
            'punta-de-ganso-angus':'vacuno','punta-picana-angus-origen-copia':'vacuno','sobrecostilla-seleccionado-pieza':'vacuno','tapabarriga-pieza-seleccionado':'vacuno','tomahawk-angus-origencongelado':'vacuno',
            'bistecpechuga':'pollo','filetillo-crocante-de-pollo':'pollo','pechuga-entera-de-pollo-deshuesado':'pollo','truto-parrillero':'pollo','bocaditos':'pollo','filetillo-de-pollo':'pollo',
            'trutro-corto-de-pollo':'pollo','trutro-largo-de-pollo':'pollo','trutro-entero':'pollo','trutrito-de-ala':'pollo','pechuga-crocante':'pollo','pollo-entero':'pollo',
        },
        'extractor': extract_procarne,
        'columns': ['Tienda','Categoria','Corte','Nombre Pagina','Precio x KG(neto)','precio pagina']
    },
}