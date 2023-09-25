
---

# Aplicación para Extraer y Visualizar Perfil MASW2D

## Descripción del programa

Esta aplicación está diseñada para visualizar y extraer perfiles de velocidad de ondas de corte (Vs) a partir de datos MASW2D. El programa acepta archivos en formato XYZ y ofrece una variedad de funcionalidades para analizar los datos, incluida la visualización en 2D, la extracción de perfiles de velocidad y la descarga de estos perfiles.

## Características

1. **Carga de Archivos**: Sube tu archivo en formato XYZ para empezar.
2. **Visualización del DataFrame**: Muestra los primeros registros del archivo cargado.
3. **Visualización de la Grilla**: Representa los datos en una grilla 2D con diversas opciones de visualización (`grid`, `scale`, `contour`).
4. **Extracción del Perfil**: Extrae un perfil de velocidad de ondas de corte (Vs) a una distancia específica.
5. **Gráficos de Perfil Extraído**: Visualiza el perfil extraído en un gráfico 2D.
6. **Descarga del Perfil**: Descarga el perfil extraído en formato CSV con opciones para tipos de extracción (`default`, `delta`, `rango`).

## Uso

1. **Subir Archivo**: Utiliza la opción de carga para subir un archivo en formato XYZ.
2. **Especificar Distancia**: Ingresa la distancia en la que deseas extraer el perfil.
3. **Extraer Perfil**: Haz clic en "Extraer Perfil" para obtener el perfil de Vs a la distancia especificada.
4. **Visualizar Perfil**: Usa el botón "Graficar Perfil Extraído" para ver el perfil en un gráfico 2D.
5. **Preparar Descarga**: Selecciona el tipo de extracción y, si es necesario, ingresa parámetros adicionales. Luego, haz clic en "Preparar Descarga CSV" para preparar el archivo para la descarga.
6. **Descargar Archivo**: Descarga el perfil en formato CSV.

6.1 **default**: Descarga el perfil unidimencional en formato "Profundidad, Vs" con la profundidad en orden decreciente

6.2 **delta**: Descarga del perfil con un `delta` de profundidad digamos si delta = 1, entonces @1m se obtendra la velocidad de ondas de corte.

6.3 **rango**: Descarga del perfil con un `rango` establecido en formato de lista '[]' donde se tiene que ingresar las profundidades puntuales a las cuales se obtendra el Vs, ejemplo '[1,1.5,3,6]'


## Requisitos

- Python 3.8
- Streamlit
- Matplotlib
- Pandas
- NumPy

detallado en el archivo requirements.txt

## Instalación

Puedes clonar este repositorio o descargarlo como ZIP. Para instalar las dependencias, navega hasta el directorio del proyecto y ejecuta:

```bash
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la aplicación, navega hasta el directorio del proyecto y ejecuta:

```bash
streamlit run app_masw_2Dto1D.py
```

---

