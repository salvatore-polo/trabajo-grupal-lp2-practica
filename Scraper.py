import requests
import time

def descargar_pagina_mercadolibre(url):
    """
    Función que se encarga de la petición HTTP a Mercado Libre.
    Acepta una URL específica como parámetro para soportar la paginación.
    """
    # El "Pase VIP" de Googlebot para evitar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    try:
        print(f"Descargando HTML desde -> {url}")
        respuesta = requests.get(url, headers=headers)
        
        # Verificamos si la conexión fue exitosa (Código 200)
        if respuesta.status_code == 200:
            print("¡Conexión exitosa! HTML descargado.")
            return respuesta.text
        else:
            print(f"Error. Código de estado: {respuesta.status_code}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error de red: {e}")
        return None

from bs4 import BeautifulSoup

def extraer_datos(html_bruto):
    """
    Toma el HTML descargado y extrae Título, Precio y Link de las laptops.
    """
    if not html_bruto: return []
    sopa = BeautifulSoup(html_bruto, 'html.parser')
    lista_laptops = []
    
    # Buscamos 'li' o 'div' que contengan la clase principal de los items
    elementos = sopa.find_all(['li', 'div'], class_=lambda c: c and 'ui-search-layout__item' in c)
    
    return lista_laptops

# Bloque de prueba rápido
if __name__ == "__main__":
    # Probamos con la página 2 para confirmar que funciona
    url_prueba = "https://listado.mercadolibre.com.pe/laptop_Desde_49"
    html_descargado = descargar_pagina_mercadolibre(url_prueba)
    
    if html_descargado:
        print(f"¡Listo! Se descargaron {len(html_descargado)} caracteres de código fuente.")##comit = "Función de descarga mejorada con soporte para paginación y manejo de errores robusto."
