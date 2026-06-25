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
