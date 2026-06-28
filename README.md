![LogoDAEI.png](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR0j2b53tAdK5qjHeX5PAgkpeNxW6ndQM5ckf-zIf8GwLfRhIbb46zPFCZb&s=10)
## --------------------- **Trabajo Grupal** ---------------------
#### **Curso:** Lenguaje de Programación II
#### **Docente:** Denise Rosalyn Chalán Llajaruna
#### **Fecha de entrega:** Martes 30 de junio de 2026
#### **Integrantes:**
- Guerrero Martínez, Jerson Julinho | 20241392 | Usuario: jersonguerrero2504
- Maguiña Tabory, Leonardo Fabio | 20241388 | Usuario: e0lab
- Polo D'Arrigo, Salvatore Diego | 20241394 | Usuario: salvatore-polo
- Potosino Apaza, Andy Weber | 20241613 | Usuario: skinsz20
- Quispe López, Daiby Jaime | 20241396 | Usuario: deiby-jql
- Salazar Vásquez, Ytzel Aleeza | 20240733 | Usuario: ytzelsalazar
#### Grupo D

## Análisis de ofertas de laptops en Mercado Libre Perú
En Mercado Libre Perú, la oferta de laptops es un negocio bastante frecuente con respecto a sus ventas. Cada laptop tiene ciertas variables a estudiar, como su capacidad de almacenamiento, memoria RAM, marca, etc. El presente estudio busca realizar un análisis de las ofertas de estas laptops en esta plataforma de compras agarrando 3 variables de estudio:
- Almacenamiento de la laptop (en GB)
- Marca de la laptop
- Precio de la laptop (en S/.)

Se usará el siguiente enlace para el estudio: [https://listado.mercadolibre.com.pe/laptop](https://listado.mercadolibre.com.pe/laptop)  
En el presente proyecto se hará lo siguiente:
- **Request:** Para poder acceder al enlace respectivo.
- **WebScraping:** Extraer los títulos de una muestra de laptops, el cual contienen la información de interés.
- **Regex:** Extraer de los títulos obtenidos la información importante (Almacenamiento, marca y precio).
- **Pandas:** Organizar los datos obtenidos en un DataFrame con el uso de pandas.
- **Visualización:** Elaboración de gráficos para hallar resultados y relaciones en las variables.
## Objetivos
### Objetivo general
- Evaluar la relación entre las variables de interés en las ofertas de laptops provenientes de Mercado Libre Perú.
### Objetivos específicos
- Comparar la distribución de precios según la marca de la laptop.
- Exponer la relación entre precios y almacenamiento en las laptops.
- Registrar los precios promedios entre las marcas y el almacenamiento en las laptops.
## Instalación
Para poder correr el respectivo proyecto se necesita tener instalado los siguientes complementos:
- Python v. 3.14
- VisualStudio Code
- Siguientes módulos de Python:
  - matplotlib.pyplot
  - seaborn
  - pandas
  - re
  - requests
  - time
  - bs4
## Estructura
El proyecto está organizado de la siguiente manera:
- README.md: Contiene información importante del proyecto.
- Reporte Trabajo Grupal.ipynb: Contiene el código del análisis hecho.
- Scraper.py/regex.py: Paquetes hechos manualmente para realizar diversas funciones con mayor facilidad.
- requiriments.txt: Blog de notas con los paquetes requeridos a instalar para el proyecto.
- Gráficos en PNG: Gráficos obtenidos en el análisis.
## Resultados
Los resultados obtenidos en el análisis son:
- Se observó que Asus es la marca que registra los precios más altos, donde estas se concentran mayormente en laptops con mayor capacidad de almacenamiento. Además se observó que tienen la mayor variabilidad de precios entre las 4 marcas.
- Se determinó que la menor variabilidad de precios de laptops se encuentra en la marca HP, indicando que gran parte de sus laptops frecuentan a tener precios poco distantes entre sí.
- Existe una tendencia positiva entre la relación entre almacenamiento y precio. En general, los equipos con mayor capacidad de almacenamiento tienden a tener precios más elevados. Sin embargo, esta relación no es lineal ya que existen varias laptops con la misma capacidad de almacenamiento y frecuentan tener precios muy variados.
