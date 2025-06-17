import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

# Configuración inicial
st.set_page_config(page_title="Garage Calculator V1", layout="centered")

st.title("Garage Tile Designer Final")

# Unidad de medida
unidad = st.selectbox("Selecciona la unidad de medida", ["centímetros", "metros"])

factor = 1 if unidad == "centímetros" else 100  # Para convertir a cm

# Dimensiones del espacio
ancho_cm = st.number_input("Ancho del espacio ({}):".format(unidad), min_value=40.0, step=10.0) * factor / 100
largo_cm = st.number_input("Largo del espacio ({}):".format(unidad), min_value=40.0, step=10.0) * factor / 100

# Dimensiones reales en metros
area_m2 = round(ancho_cm * largo_cm, 2)
st.markdown(f"**Área total:** {area_m2} m²")

# Opciones bordillos y esquineros
agregar_bordillos = st.checkbox("Agregar bordillos", value=True)
agregar_esquineros = st.checkbox("Agregar esquineros", value=True)

posiciones_bordillo = []
if agregar_bordillos:
    posiciones_bordillo = st.multiselect("¿Dónde colocar bordillos?", ["Arriba", "Abajo", "Izquierda", "Derecha"],
                                         default=["Arriba", "Abajo", "Izquierda", "Derecha"])

# Colores disponibles
colores = {
    "Negro": "#000000",
    "Gris": "#A9A9A9",
    "Gris Oscuro": "#555555",
    "Azul": "#0000FF",
    "Celeste": "#00BFFF",
    "Amarillo": "#FFD700",
    "Verde": "#228B22",
    "Rojo": "#FF0000",
    "Blanco": "#FFFFFF"
}

st.subheader("Color base")
color_base = st.selectbox("Color base", list(colores.keys()))
color_hex = colores[color_base]

# Botón para aplicar el color
if st.button("Aplicar color base"):
    st.session_state["aplicar_color"] = True
    st.session_state["color_actual"] = color_base

# Cálculo de cantidad de palmetas
lado_palmeta = 0.4  # 40 cm = 0.4 m
cols = math.ceil(ancho_cm / lado_palmeta)
rows = math.ceil(largo_cm / lado_palmeta)
total_palmetas = rows * cols

# Bordillos por lado (1 por palmeta en cada lado seleccionado)
bordillos = 0
if agregar_bordillos:
    if "Arriba" in posiciones_bordillo:
        bordillos += cols
    if "Abajo" in posiciones_bordillo:
        bordillos += cols
    if "Izquierda" in posiciones_bordillo:
        bordillos += rows
    if "Derecha" in posiciones_bordillo:
        bordillos += rows

# Esquineros siempre 4 si se selecciona
esquineros = 4 if agregar_esquineros else 0

# Mostrar cantidad
st.markdown("### Cantidad necesaria:")
st.markdown(f"""
- **Palmetas:** {total_palmetas}  
- **Bordillos:** {bordillos}  
- **Esquineros:** {esquineros}
""")

# Crear la grilla de diseño
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal')
plt.axis('off')

# Dibujar palmetas
for y in range(rows):
    for x in range(cols):
        edge = "white" if color_base == "Negro" else "black"
        ax.add_patch(plt.Rectangle((x, rows - 1 - y), 1, 1, facecolor=color_hex, edgecolor=edge))

# Dibujar bordillos
if agregar_bordillos:
    for x in range(cols):
        if "Abajo" in posiciones_bordillo:
            ax.add_patch(plt.Rectangle((x, -0.15), 1, 0.15, color='black'))
        if "Arriba" in posiciones_bordillo:
            ax.add_patch(plt.Rectangle((x, rows), 1, 0.15, color='black'))
    for y in range(rows):
        if "Izquierda" in posiciones_bordillo:
            ax.add_patch(plt.Rectangle((-0.15, y), 0.15, 1, color='black'))
        if "Derecha" in posiciones_bordillo:
            ax.add_patch(plt.Rectangle((cols, y), 0.15, 1, color='black'))

# Dibujar esquineros
if agregar_esquineros:
    ax.add_patch(plt.Rectangle((-0.15, -0.15), 0.15, 0.15, color='black'))  # Inferior izquierda
    ax.add_patch(plt.Rectangle((cols, -0.15), 0.15, 0.15, color='black'))  # Inferior derecha
    ax.add_patch(plt.Rectangle((-0.15, rows), 0.15, 0.15, color='black'))  # Superior izquierda
    ax.add_patch(plt.Rectangle((cols, rows), 0.15, 0.15, color='black'))  # Superior derecha

# Líneas de medida
line_offset = 0.5
ax.annotate(f"{round(cols * lado_palmeta, 2)} m", xy=(cols / 2, rows + 0.6),
            ha='center', fontsize=12)
ax.annotate("", xy=(0, rows + 0.4), xytext=(cols, rows + 0.4),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='gray'))
ax.annotate("", xy=(cols, rows + 0.4), xytext=(0, rows + 0.4),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='gray'))

ax.annotate(f"{round(rows * lado_palmeta, 2)} m", xy=(cols + 0.6, rows / 2),
            va='center', fontsize=12, rotation=270)
ax.annotate("", xy=(cols + 0.4, 0), xytext=(cols + 0.4, rows),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='gray'))
ax.annotate("", xy=(cols + 0.4, rows), xytext=(cols + 0.4, 0),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='gray'))

st.pyplot(fig)
