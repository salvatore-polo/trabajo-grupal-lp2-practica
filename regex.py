import re

MARCAS_CONOCIDAS = [
    "HP", "Lenovo", "Dell", "Asus", "Acer", "Apple", "MacBook",
    "Samsung", "Huawei", "MSI", "Toshiba", "Microsoft", "LG",
    "Gateway", "Compaq", "Vaio", "Sony"
]

SUB_MARCAS = {
    "victus": "HP", "omen": "HP", "pavilion": "HP", "probook": "HP", "elitebook": "HP",
    "ideapad": "Lenovo", "thinkpad": "Lenovo", "legion": "Lenovo", "loq": "Lenovo", "yoga": "Lenovo",
    "vivobook": "Asus", "zenbook": "Asus", "rog": "Asus", "tuf": "Asus",
    "inspiron": "Dell", "xps": "Dell", "latitude": "Dell", "vostro": "Dell",
    "predator": "Acer", "nitro": "Acer", "aspire": "Acer", "swift": "Acer",
    "galaxy book": "Samsung",
}

def extraer_marca(titulo):
    for marca in MARCAS_CONOCIDAS:
        patron = r"\b" + re.escape(marca) + r"\b"
        if re.search(patron, titulo, re.IGNORECASE):
            if marca.lower() == "macbook":
                return "Apple"
            return marca

    for sub_marca, marca_real in SUB_MARCAS.items():
        if re.search(r"\b" + re.escape(sub_marca) + r"\b", titulo, re.IGNORECASE):
            return marca_real

    return "Desconocida"

def _extraer_memoria(titulo):
    texto = titulo

    patron_storage = re.compile(r"\b(\d{1,4})\s*(GB|TB)?\s*(SSD|HDD|eMMC)\b", re.IGNORECASE)
    patron_storage_rev = re.compile(r"\b(SSD|HDD|eMMC)\s*(\d{1,4})\s*(GB|TB)?\b", re.IGNORECASE)

    almacenamiento = None
    tipo = "Desconocido"
    span_storage = None

    m_storage = patron_storage.search(texto)
    if m_storage:
        valor = int(m_storage.group(1))
        if m_storage.group(2) and m_storage.group(2).upper() == "TB":
            valor *= 1024
        almacenamiento = valor
        tipo = m_storage.group(3).upper()
        span_storage = m_storage.span()
    else:
        m_storage_rev = patron_storage_rev.search(texto)
        if m_storage_rev:
            valor = int(m_storage_rev.group(2))
            if m_storage_rev.group(3) and m_storage_rev.group(3).upper() == "TB":
                valor *= 1024
            almacenamiento = valor
            tipo = m_storage_rev.group(1).upper()
            span_storage = m_storage_rev.span()

    def se_solapa(span):
        return span_storage and not (span[1] <= span_storage[0] or span[0] >= span_storage[1])

    ram = None
    span_ram = None
    patron_ram_1 = re.compile(r"\b(\d{1,4})\s*(GB|TB)\s*(?:de\s*)?(?:Ram\b|Memoria)", re.IGNORECASE)
    patron_ram_2 = re.compile(r"\bRam\s*(\d{1,4})\s*(GB|TB)\b", re.IGNORECASE)
    patron_ram_3 = re.compile(r"\b(\d{1,3})\s*Ram\b", re.IGNORECASE)

    m_ram = patron_ram_1.search(texto)
    if m_ram and not se_solapa(m_ram.span()):
        valor = int(m_ram.group(1))
        if m_ram.group(2).upper() == "TB":
            valor *= 1024
        ram = valor
        span_ram = m_ram.span()
    else:
        m_ram2 = patron_ram_2.search(texto)
        if m_ram2 and not se_solapa(m_ram2.span()):
            valor = int(m_ram2.group(1))
            if m_ram2.group(2).upper() == "TB":
                valor *= 1024
            ram = valor
            span_ram = m_ram2.span()
        else:
            m_ram3 = patron_ram_3.search(texto)
            if m_ram3 and not se_solapa(m_ram3.span()):
                valor = int(m_ram3.group(1))
                if 2 <= valor <= 128:
                    ram = valor
                    span_ram = m_ram3.span()

    patron_generico = re.compile(r"\b(\d{1,4})\s*(GB|TB)\b", re.IGNORECASE)
    restantes = []
    for gm in patron_generico.finditer(texto):
        span = gm.span()
        if se_solapa(span):
            continue
        if span_ram and not (span[1] <= span_ram[0] or span[0] >= span_ram[1]):
            continue
        valor = int(gm.group(1))
        if gm.group(2).upper() == "TB":
            valor *= 1024
        restantes.append(valor)

    es_apple = bool(re.search(r"apple|macbook", texto, re.IGNORECASE))

    if ram is None and almacenamiento is None:
        if len(restantes) >= 2:
            ram, almacenamiento = restantes[0], restantes[1]
        elif len(restantes) == 1:
            if es_apple:
                almacenamiento = restantes[0]
                tipo = "SSD"
            else:
                ram = restantes[0]
    elif ram is None and restantes:
        ram = restantes[0]
    elif almacenamiento is None and restantes:
        almacenamiento = restantes[0]

    if es_apple and almacenamiento is not None and tipo == "Desconocido":
        tipo = "SSD"

    if ram is not None and almacenamiento is not None and ram > almacenamiento:
        ram, almacenamiento = almacenamiento, ram

    return ram, almacenamiento, tipo


def extraer_ram(titulo):
    ram, _, _ = _extraer_memoria(titulo)
    return ram


def extraer_almacenamiento(titulo):
    _, almacenamiento, _ = _extraer_memoria(titulo)
    return almacenamiento


def extraer_tipo_almacenamiento(titulo):
    _, _, tipo = _extraer_memoria(titulo)
    return tipo

def extraer_titulo_limpio(titulo):
    return re.sub(r"\s+", " ", titulo).strip()


def procesar_laptops(lista_laptops):
    lista_titulo = []
    lista_marca = []
    lista_ram = []
    lista_almacenamiento = []
    lista_tipo_almacenamiento = []
    lista_precio = []
    lista_link = []

    for laptop in lista_laptops:
        titulo_crudo = laptop.get("titulo_crudo", "")

        lista_titulo.append(extraer_titulo_limpio(titulo_crudo))
        lista_marca.append(extraer_marca(titulo_crudo))
        lista_ram.append(extraer_ram(titulo_crudo))
        lista_almacenamiento.append(extraer_almacenamiento(titulo_crudo))
        lista_tipo_almacenamiento.append(extraer_tipo_almacenamiento(titulo_crudo))

        precio_raw = laptop.get("precio", "0")
        try:
            lista_precio.append(int(precio_raw))
        except (ValueError, TypeError):
            lista_precio.append(None)

        lista_link.append(laptop.get("link", "Sin link"))

    return (
        lista_titulo,
        lista_marca,
        lista_ram,
        lista_almacenamiento,
        lista_tipo_almacenamiento,
        lista_precio,
        lista_link,
    )


if __name__ == "__main__":
    from Scraper import descargar_pagina_mercadolibre, extraer_datos

    url_prueba = "https://listado.mercadolibre.com.pe/laptop"
    html_descargado = descargar_pagina_mercadolibre(url_prueba)

    if html_descargado:
        laptops = extraer_datos(html_descargado)

        if laptops:
            (lista_titulo, lista_marca, lista_ram, lista_almacenamiento,
             lista_tipo_almacenamiento, lista_precio, lista_link) = procesar_laptops(laptops)

            print("Lista Marca:", lista_marca)
            print("Lista Almacenamiento:", lista_almacenamiento)
            print("Lista Precio:", lista_precio)
