import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

st.set_page_config(layout="centered")
st.title("Garage Tile Designer Final")

# --- Inputs de usuario ---
unidad = st.selectbox("Selecciona la unidad de medida", ["centímetros", "metros"])
factor = 0.01 if unidad == "centímetros" else 1.0

ancho = st.number_input(f"Ancho del espacio ({unidad})", min_value=40.0, step=10.0) * factor
largo = st.number_input(f"Largo del espacio ({unidad})", min_value=40.0, step=10.0) * factor
area_m2 = round(ancho * largo, 2)
st.markdown(f"**Área total:** {area_m2} m²")

agregar_bordillos = st.checkbox("Agregar bordillos", value=True)
agregar_esquineros = st.checkbox("Agregar esquineros", value=True)
lados_bordillos = st.multiselect("¿Dónde colocar bordillos?", ["Arriba", "Abajo", "Izquierda", "Derecha"], default=["Arriba", "Abajo", "Izquierda", "Derecha"])

# --- Parámetros de palmetas ---
TILE_CM = 40
TILE_M = TILE_CM / 100
cols = int(np.ceil(ancho / TILE_M))
rows = int(np.ceil(largo / TILE_M))
real_ancho = cols * TILE_M
real_largo = rows * TILE_M

# --- Colores disponibles ---
colores_palmetas = {
    "Negro": "#000000",
    "Gris": "#BEBEBE",
    "Gris Oscuro": "#4F4F4F",
    "Azul": "#4682B4",
    "Celeste": "#87CEFA",
    "Amarillo": "#FFD700",
    "Verde": "#228B22",
    "Rojo": "#FF0000",
    "Blanco": "#FFFFFF"
}
color_base = st.selectbox("Color base", list(colores_palmetas.keys()))
color_hex = colores_palmetas[color_base]

if st.button("Aplicar color base"):
    pass

# --- Cálculo de bordillos y esquineros ---
bordillos = 0
if agregar_bordillos:
    if "Arriba" in lados_bordillos: bordillos += cols
    if "Abajo" in lados_bordillos: bordillos += cols
    if "Izquierda" in lados_bordillos: bordillos += rows
    if "Derecha" in lados_bordillos: bordillos += rows
esquineros = 4 if agregar_esquineros else 0
total_tiles = rows * cols

# --- Mostrar resumen ---
st.markdown("### Cantidad necesaria:")
st.markdown(f"- **Palmetas:** {total_tiles}")
st.markdown(f"- **Bordillos:** {bordillos}")
st.markdown(f"- **Esquineros:** {esquineros}")

# --- Visualización ---
fig, ax = plt.subplots(figsize=(cols, rows))
for y in range(rows):
    for x in range(cols):
        ax.add_patch(patches.Rectangle(
            (x, rows - 1 - y),
            1, 1,
            facecolor=color_hex,
            edgecolor="white" if color_base == "Negro" else "black"
        ))

# --- Bordillos ---
if agregar_bordillos:
    for x in range(cols):
        if "Arriba" in lados_bordillos:
            ax.add_patch(patches.Rectangle((x, rows), 1, 0.15, facecolor="black", edgecolor="white" if color_base == "Negro" else "black"))
        if "Abajo" in lados_bordillos:
            ax.add_patch(patches.Rectangle((x, -0.15), 1, 0.15, facecolor="black", edgecolor="white" if color_base == "Negro" else "black"))
    for y in range(rows):
        if "Izquierda" in lados_bordillos:
            ax.add_patch(patches.Rectangle((-0.15, y), 0.15, 1, facecolor="black", edgecolor="white" if color_base == "Negro" else "black"))
        if "Derecha" in lados_bordillos:
            ax.add_patch(patches.Rectangle((cols, y), 0.15, 1, facecolor="black", edgecolor="white" if color_base == "Negro" else "black"))

# --- Esquineros ---
if agregar_esquineros:
    esquinas = [(-0.15, -0.15), (cols, -0.15), (-0.15, rows), (cols, rows)]
    for (x, y) in esquinas:
        ax.add_patch(patches.Rectangle((x, y), 0.15, 0.15, facecolor="black", edgecolor="white" if color_base == "Negro" else "black"))

# --- Etiquetas de medida reales ---
ax.plot([0, cols], [rows + 0.4, rows + 0.4], color="gray")
ax.text(cols / 2, rows + 0.5, f"{real_ancho:.2f} m", ha="center", va="bottom")
ax.plot([cols + 0.4, cols + 0.4], [0, rows], color="gray")
ax.text(cols + 0.5, rows / 2, f"{real_largo:.2f} m", va="center", ha="left", rotation=90)

# --- Área ingresada (en rojo) ---
tiles_ancho_usuario = ancho / TILE_M
tiles_largo_usuario = largo / TILE_M
x_offset = (cols - tiles_ancho_usuario) / 2
y_offset = (rows - tiles_largo_usuario) / 2

ax.add_patch(patches.Rectangle(
    (x_offset, y_offset),
    tiles_ancho_usuario,
    tiles_largo_usuario,
    edgecolor="red",
    linestyle="--",
    linewidth=2,
    facecolor="none"
))

ax.set_xlim(-0.5, cols + 1)
ax.set_ylim(-0.5, rows + 1)
ax.set_aspect("equal")
ax.axis("off")
st.pyplot(fig)
