#%% Impotación de Librerias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import griddata

#%% Definición de funciones principales

# Function to plot 2D profile (MASW2D)
def graficar_perfil2D_v0(data):
    plt.figure(figsize=(12, 6))
    plt.scatter(data['X'], data['Y'], c=data['Vs'], cmap='viridis', s=5)
    plt.colorbar(label='Vs (Velocidad de ondas de corte, m/s)')
    plt.xlabel('X (Ubicación en línea sísmica)')
    plt.ylabel('Y (Cota topográfica)')
    plt.title('Perfil MASW2D (Mapa de Calor)')
    #plt.gca().invert_yaxis()
    st.pyplot(plt)


def graficar_perfil2D(data, tipo_grafico='grid', delta_velocidad=20):
    plt.figure(figsize=(12, 6))

    x = data['X']
    y = data['Y']
    vs = data['Vs']
    cmap = 'RdYlGn'

    if tipo_grafico == 'grid':
        plt.scatter(x, y, c=vs, cmap=cmap, s=5)
    else:
        xi, yi = np.linspace(x.min(), x.max(), 500), np.linspace(y.min(), y.max(), 500)
        xi, yi = np.meshgrid(xi, yi)
        zi = griddata((x, y), vs, (xi, yi), method='linear')

        vmax_with_delta = 10 * ((vs.max() + 2*delta_velocidad)//10)  # Include delta in the max value
        
        if tipo_grafico == 'scale':
            plt.imshow(zi, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap=cmap, aspect='auto', vmin=10 * (vs.min()//10), vmax=vmax_with_delta)
        elif tipo_grafico == 'contour':
            levels = np.arange(vs.min(), vmax_with_delta, delta_velocidad)
            plt.contourf(xi, yi, zi, levels=levels, cmap=cmap, extend='max')  # Ensure extending to max value
            plt.contour(xi, yi, zi, levels=levels, colors='black', linewidths=0.5)

    plt.colorbar(label='Vs (Velocidad de ondas de corte, m/s)')
    plt.xlabel('X (Ubicación en línea sísmica)')
    plt.ylabel('Y (Cota topográfica)')
    plt.title('Perfil MASW2D (Mapa de Calor)')
    st.pyplot(plt)



# Modified function to extract the velocity profile at a given distance
def extraer_perfil_X_corregido(distancia, data):
    # Selecting data at the specified distance
    perfil_data = data[data['X'] == distancia][['Y', 'Vs']]
    # Finding the surface elevation (maximum Y value)
    cota_superficie = perfil_data['Y'].max()
    # Calculating depth by subtracting surface elevation and taking absolute value
    perfil_data['Y'] = (perfil_data['Y'] - cota_superficie).abs()
    # Renaming columns to represent depth and velocity
    perfil_data.columns = ['Profundidad', 'Velocidad (m/s)']
    return perfil_data


#%%
# Function to plot the velocity profile with a stepped appearance
def graficar_perfil_escalones(perfil_data, distancia):
    plt.figure(figsize=(8, 6))
    plt.step(perfil_data['Velocidad (m/s)'], perfil_data['Profundidad'], where='post', color='red', label=f'Distancia = {distancia} m')
    plt.xlabel('Velocidad de ondas de corte (m/s)')
    plt.ylabel('Profundidad (m)')
    plt.title('Perfil de Velocidades (Apariencia Escalonada)')
    plt.legend()
    plt.grid(color='lightgray', linestyle='-', linewidth=0.5)  # Adding grid lines
    plt.gca().invert_yaxis()  # Inverting Y-axis to represent depth
    st.pyplot(plt)


# Function to extract the profile to a CSV file
def extraer_csv(perfil_extraido, tipo_extraccion, profundidad=1, vector_profundidad=None):
    perfil_to_save = perfil_extraido.copy()

    # Handling different extraction types
    if tipo_extraccion == 'delta':
        vector_profundidad = np.arange(profundidad, perfil_extraido['Profundidad'].max(), profundidad)
        interpolator = interp1d(perfil_extraido['Profundidad'], perfil_extraido['Velocidad (m/s)'], kind='linear', fill_value='extrapolate')
        velocities = interpolator(vector_profundidad)
        perfil_to_save = pd.DataFrame({'Profundidad': vector_profundidad, 'Velocidad (m/s)': velocities})
    elif tipo_extraccion == 'rango':
        interpolator = interp1d(perfil_extraido['Profundidad'], perfil_extraido['Velocidad (m/s)'], kind='linear', fill_value='extrapolate')
        velocities = interpolator(vector_profundidad)
        perfil_to_save = pd.DataFrame({'Profundidad': vector_profundidad, 'Velocidad (m/s)': velocities})
    
    # Converting the DataFrame to CSV format
    csv = perfil_to_save.to_csv(index=False)
    return csv



#%% Main application
def main():
    st.title("Aplicación para Extraer y Visualizar Perfil MASW2D")

    st.text("""
    Descripción del programa:
    Esta aplicación permite cargar un archivo XYZ de velocidad, extraer un perfil de velocidades para una distancia específica,
    graficar este perfil y finalmente extraer y descargar el perfil en formato CSV.

    """)

    uploaded_file = st.file_uploader("Subir archivo XYZ:", type=['xyz', 'txt'])

    if uploaded_file:
        st.success("Archivo cargado con éxito.")
        data = pd.read_csv(uploaded_file, sep=' +', engine='python', names=['X', 'Y', 'Vs'])

        st.subheader("Visualización del DataFrame del Archivo")
        st.dataframe(data.head())

        st.subheader("Visualización de la Grilla del Archivo XYZ")
        
        tipo_grafico = st.selectbox("Seleccionar Tipo de Grafico de XYZ:", ['grid', 'scale', 'contour'], key='tipo_grafico')
        
        if tipo_grafico != 'grid':
            if tipo_grafico == 'scale':
                graficar_perfil2D(data,'scale')
                
            else:
                delta_velocidad = st.number_input("Introducir el delta del contorno de velocidad:", min_value=20, value=50)
                graficar_perfil2D(data,'contour', delta_velocidad)

        else:        
            graficar_perfil2D(data)

        distancia = st.number_input("Introducir la distancia de extracción del perfil:", min_value=0, value=30)

        if st.button("Extraer Perfil"):
            # Extracting profile
            perfil_extraido = extraer_perfil_X_corregido(distancia, data)
            st.session_state.perfil_extraido = perfil_extraido  # Storing in session state
            st.success("Perfil extraído exitosamente.")

        if st.button("Graficar Perfil Extraído"):
            # Retrieving from session state
            perfil_extraido = st.session_state.get('perfil_extraido', None)
            if perfil_extraido is not None:
                st.subheader("Gráfico del Perfil Extraído")
                graficar_perfil_escalones(perfil_extraido, distancia)
            else:
                st.warning("Por favor, extraiga el perfil primero.")

        tipo_extraccion = st.selectbox("Seleccionar Tipo de Extracción:", ['default', 'delta', 'rango'], key='tipo_extraccion')
        parametro_extra = None

        if tipo_extraccion != 'default':
            key = f"input_{tipo_extraccion}"
            parametro_extra_str = st.text_input(f"Ingresar Parámetro para Extracción '{tipo_extraccion}':", key=key)
            if parametro_extra_str: # Convert only if not empty
                if tipo_extraccion == 'delta':
                    parametro_extra = float(parametro_extra_str)
                elif tipo_extraccion == 'rango':
                    parametro_extra = [float(x) for x in parametro_extra_str.strip('[]').split(',')]

        perfil_extraido = st.session_state.get('perfil_extraido', None) # Retrieving from session state
        if perfil_extraido is not None:
            csv = extraer_csv(perfil_extraido, tipo_extraccion, profundidad=parametro_extra, vector_profundidad=parametro_extra)
            # Converting CSV to bytes
            csv_bytes = csv.encode('utf-8')
            st.download_button("Descargar archivo CSV", csv_bytes, file_name="perfil_extraido.csv", mime="text/csv")
        elif st.button("Preparar Descarga CSV"):
            st.warning("Por favor, extraiga el perfil primero.")

        



#%%

if __name__ == "__main__":
    main()
