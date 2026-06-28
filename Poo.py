import requests
from bs4 import BeautifulSoup

class MercadoLibreApi:

    def obtener_datos(self, url):
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        }

        try:
            print(f"Descargando HTML desde -> {url}")
            respuesta = requests.get(url, headers=headers)

            if respuesta.status_code != 200:
                print(f"Error. Código de estado: {respuesta.status_code}")
                return []

            print("¡Conexión exitosa! HTML descargado.")

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

                etiqueta_precio = item.find(
                    "span",
                    class_="andes-money-amount__fraction"
                )
                precio = (
                    etiqueta_precio.get_text(strip=True).replace(".", "")
                    if etiqueta_precio else "0"
                )

                if len(titulo) > 10 and precio != "0":
                    lista_laptops.append({
                        "titulo_crudo": titulo,
                        "precio": precio,
                        "link": link
                    })

            return lista_laptops

        except requests.exceptions.RequestException as e:
            print(f"Error de red: {e}")
            return []

import re

class ExtractorRegex:

    def extraer_marca(self, titulo):
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

    def procesar_laptops(self, lista_laptops):
        lista_titulo = []
        lista_marca = []
        lista_ram = []
        lista_almacenamiento = []
        lista_tipo_almacenamiento = []
        lista_precio = []
        lista_link = []

        for laptop in lista_laptops:
            titulo = laptop.get("titulo_crudo", "")

            lista_titulo.append(self.extraer_titulo(titulo))
            lista_marca.append(self.extraer_marca(titulo))
            lista_ram.append(self.extraer_ram(titulo))
            lista_almacenamiento.append(self.extraer_almacenamiento(titulo))
            lista_tipo_almacenamiento.append(self.extraer_tipo_almacenamiento(titulo))

            try:
                lista_precio.append(int(laptop.get("precio", "0")))
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
    
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Analizador:

    def crear_dataframe(self, lista_marca, lista_almacenamiento, lista_precio):
        dicc = {
            "Marca": lista_marca,
            "Almacenamiento": lista_almacenamiento,
            "Lista Precio": lista_precio
        }

        self.DataFrameDatos = pd.DataFrame(dicc)
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

if __name__ == "__main__":

    url = "https://listado.mercadolibre.com.pe/laptop"

    api = MercadoLibreApi()
    lista_laptops = api.obtener_datos(url)

    regex = ExtractorRegex()

    (
        lista_titulo,
        lista_marca,
        lista_ram,
        lista_almacenamiento,
        lista_tipo_almacenamiento,
        lista_precio,
        lista_link
    ) = regex.procesar_laptops(lista_laptops)

    analizador = Analizador()

    df = analizador.crear_dataframe(
        lista_marca,
        lista_almacenamiento,
        lista_precio
    )

    print(df)

    analizador.grafico1()
    analizador.grafico2()
    analizador.grafico3()
