import requests
from bs4 import BeautifulSoup

class MercadoLibreApi:

    def __init__(self, url):
        self.url = url

    def obtener_datos(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }

        try:
            respuesta = requests.get(self.url, headers=headers)

            if respuesta.status_code != 200:
                return []

            sopa = BeautifulSoup(respuesta.text, "html.parser")
            lista_laptops = []

            elementos = sopa.find_all(
                ["li", "div"],
                class_=lambda c: c and "ui-search-layout__item" in c
            )

            for item in elementos:
                etiqueta_a = item.find("a")
                link = etiqueta_a.get("href", "Sin link") if etiqueta_a else "Sin link"

                etiqueta_titulo = item.find(["h2", "h3"])
                titulo = etiqueta_titulo.get_text(strip=True) if etiqueta_titulo else "Sin título"

                etiqueta_precio = item.find("span", class_="andes-money-amount__fraction")
                precio = etiqueta_precio.get_text(strip=True).replace(".", "") if etiqueta_precio else "0"

                if len(titulo) > 10 and precio != "0":
                    lista_laptops.append({
                        "titulo_crudo": titulo,
                        "precio": precio,
                        "link": link
                    })

            return lista_laptops

        except requests.exceptions.RequestException:
            return []

import re

class ExtractorRegex:

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

    def __init__(self, lista_laptops):
        self.lista_laptops = lista_laptops

    def extraer_marca(self, titulo):
        for marca in self.MARCAS_CONOCIDAS:
            patron = r"\b" + re.escape(marca) + r"\b"
            if re.search(patron, titulo, re.IGNORECASE):
                if marca.lower() == "macbook":
                    return "Apple"
                return marca

        for sub_marca, marca_real in self.SUB_MARCAS.items():
            if re.search(r"\b" + re.escape(sub_marca) + r"\b", titulo, re.IGNORECASE):
                return marca_real

        return "Desconocida"

    def _extraer_memoria(self, titulo):
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

    def extraer_ram(self, titulo):
        ram, _, _ = self._extraer_memoria(titulo)
        return ram

    def extraer_almacenamiento(self, titulo):
        _, almacenamiento, _ = self._extraer_memoria(titulo)
        return almacenamiento

    def extraer_tipo_almacenamiento(self, titulo):
        _, _, tipo = self._extraer_memoria(titulo)
        return tipo

    def extraer_titulo(self, titulo):
        return re.sub(r"\s+", " ", titulo).strip()

    def procesar_datos(self):
        lista_titulo = []
        lista_marca = []
        lista_ram = []
        lista_almacenamiento = []
        lista_tipo = []
        lista_precio = []
        lista_link = []

        for laptop in self.lista_laptops:
            titulo = laptop.get("titulo_crudo", "")

            lista_titulo.append(self.extraer_titulo(titulo))
            lista_marca.append(self.extraer_marca(titulo))
            lista_ram.append(self.extraer_ram(titulo))

            almacenamiento = self.extraer_almacenamiento(titulo)
            lista_almacenamiento.append(1024 if almacenamiento is None else almacenamiento)

            lista_tipo.append(self.extraer_tipo_almacenamiento(titulo))

            try:
                lista_precio.append(int(laptop.get("precio", "0")))
            except:
                lista_precio.append(None)

            lista_link.append(laptop.get("link", "Sin link"))

        return (
            lista_titulo,
            lista_marca,
            lista_ram,
            lista_almacenamiento,
            lista_tipo,
            lista_precio,
            lista_link
        )
    
import pandas as pd

class Analizador:

    def __init__(self, lista_titulo, lista_marca, lista_ram,
                 lista_almacenamiento, lista_tipo,
                 lista_precio, lista_link):

        self.lista_titulo = lista_titulo
        self.lista_marca = lista_marca
        self.lista_ram = lista_ram
        self.lista_almacenamiento = lista_almacenamiento
        self.lista_tipo = lista_tipo
        self.lista_precio = lista_precio
        self.lista_link = lista_link

    def crear_dataframe(self):
        datos = {
            "Titulo": self.lista_titulo,
            "Marca": self.lista_marca,
            "RAM": self.lista_ram,
            "Almacenamiento": self.lista_almacenamiento,
            "Tipo": self.lista_tipo,
            "Precio": self.lista_precio,
            "Link": self.lista_link
        }

        return pd.DataFrame(datos)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class Analizador:

    def __init__(self, lista_titulo, lista_marca, lista_ram,
                 lista_almacenamiento, lista_tipo,
                 lista_precio, lista_link):

        self.lista_titulo = lista_titulo
        self.lista_marca = lista_marca
        self.lista_ram = lista_ram
        self.lista_almacenamiento = lista_almacenamiento
        self.lista_tipo = lista_tipo
        self.lista_precio = lista_precio
        self.lista_link = lista_link

    def crear_dataframe(self):
        datos = {
            "Titulo": self.lista_titulo,
            "Marca": self.lista_marca,
            "RAM": self.lista_ram,
            "Almacenamiento": self.lista_almacenamiento,
            "Tipo": self.lista_tipo,
            "Lista Precio": self.lista_precio,
            "Link": self.lista_link
        }

        self.DataFrameDatos = pd.DataFrame(datos)
        return self.DataFrameDatos

    def grafico1(self):
        plt.figure(figsize=(10, 6))
        sns.boxplot(
            x="Marca",
            y="Lista Precio",
            data=self.DataFrameDatos,
            palette="Set2"
        )
        plt.title("Distribución y Variabilidad de precios por marca")
        plt.ylabel("Precio en soles")
        plt.xlabel("Marca")
        plt.show()

    def grafico2(self):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(
            x="Almacenamiento",
            y="Lista Precio",
            hue="Marca",
            style="Marca",
            markers=True,
            data=self.DataFrameDatos,
            s=100,
            alpha=0.7
        )
        plt.title("Relación entre almacenamiento y precio")
        plt.ylabel("Precio en soles")
        plt.xlabel("Almacenamiento en GB")
        plt.show()

    def grafico3(self):
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x="Marca",
            y="Lista Precio",
            hue="Almacenamiento",
            data=self.DataFrameDatos,
            palette="tab10",
            errorbar=None
        )
        plt.title("Precio Promedio por marca según su almacenamiento")
        plt.ylabel("Precio Promedio en soles")
        plt.xlabel("Marca")
        plt.legend(title="Almacenamiento en GB")
        plt.show()

from Scraper import MercadoLibreApi
from regex import ExtractorRegex
from analizador import Analizador

url = "https://listado.mercadolibre.com.pe/laptop"

api = MercadoLibreApi(url)
lista_laptops = api.obtener_datos()

regex = ExtractorRegex(lista_laptops)

(
    lista_titulo,
    lista_marca,
    lista_ram,
    lista_almacenamiento,
    lista_tipo,
    lista_precio,
    lista_link
) = regex.procesar_datos()

analizador = Analizador(
    lista_titulo,
    lista_marca,
    lista_ram,
    lista_almacenamiento,
    lista_tipo,
    lista_precio,
    lista_link
)

df = analizador.crear_dataframe()

print(df)

analizador.grafico1()
analizador.grafico2()
analizador.grafico3()