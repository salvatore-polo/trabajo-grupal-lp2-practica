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
