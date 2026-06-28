import pandas as pd

dicc = {"Marca": lista_marca, "Almacenamiento": lista_almacenamiento, "Lista Precio": lista_precio}

DataFrameDatos = pd.DataFrame(dicc)
DataFrameDatos

import matplotlib.pyplot as plt
import seaborn as sns
#Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Marca', y='Lista Precio', data=DataFrameDatos, palette='Set2')
plt.title('Distribución y Variabilidad de precios por marca')
plt.ylabel('Precio en soles')
plt.xlabel('Marca')
plt.show()


#dispersión
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Almacenamiento', y='Lista Precio', hue='Marca',style="Marca",markers=True, data=DataFrameDatos, s=100, alpha=0.7)
plt.title('Relación entre almacenamiento y precio')
plt.ylabel('Precio en soles')
plt.xlabel('Almacenamiento en GB')
plt.show()

#barras
plt.figure(figsize=(12, 6))
sns.barplot(x='Marca', y='Lista Precio', hue='Almacenamiento', data=DataFrameDatos, palette='tab10', errorbar=None)
plt.title('Precio Promedio por marca según su almacenamiento')
plt.ylabel('Precio Promedio en soles')
plt.xlabel('Marca')
plt.legend(title='Almacenamiento en GB')
plt.show()
