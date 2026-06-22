import requests

def descargar_pagina_mercadolibre():
    """
    Función que Se encarga de la petición HTTP a Mercado Libre.
    Utiliza un User-Agent de Googlebot para evadir los bloqueos de seguridad.
    """
    url = "https://listado.mercadolibre.com.pe/laptop"
    
    # El pase para que Mercado Libre no nos bloquee
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    }

    try:
        print("Realizando petición a Mercado Libre...")
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

# Bloque de prueba (solo se ejecuta si corres este archivo directamente)
if __name__ == "__main__":
    html_descargado = descargar_pagina_mercadolibre()
    if html_descargado:
        print(f"¡Listo! Se descargaron {len(html_descargado)} caracteres de código fuente.")