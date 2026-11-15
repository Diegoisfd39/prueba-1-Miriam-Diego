
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(
    page_title="Fractales geométricos",
    page_icon="🔷",
    layout="wide"
)


@st.cache_data
def nvertices(lados, modulo, x0, y0):
    angulos = np.linspace(0, 2 * np.pi, lados, endpoint=False)
    vertx = x0 + modulo * np.cos(angulos)
    verty = y0 + modulo * np.sin(angulos)
    return vertx, verty


@st.cache_data
def fractales(lados, iteraciones, modulo, semilla):
    x0, y0 = 0.0, 0.0
    vertx, verty = nvertices(lados, modulo, x0, y0)

    rng = np.random.default_rng(semilla)

    puntos_x = np.empty(iteraciones)
    puntos_y = np.empty(iteraciones)

    px, py = x0, y0

    for i in range(iteraciones):
        v = rng.integers(0, lados)

        px = (px + vertx[v]) / 2
        py = (py + verty[v]) / 2

        puntos_x[i] = px
        puntos_y[i] = py

    return puntos_x, puntos_y, vertx, verty


st.title("🔷 Explorando los fractales geométricos")

st.markdown(
    """
    Los fractales pueden surgir de la repetición de reglas matemáticas
    relativamente sencillas.

    En este experimento vamos a construir un fractal mediante un juego
    aleatorio: partimos del centro de un polígono regular y, en cada
    iteración, elegimos un vértice al azar y avanzamos hasta el punto medio
    entre nuestra posición actual y ese vértice.
    """
)

st.sidebar.header("Configuración del experimento")

lados = st.sidebar.slider(
    "Cantidad de lados del polígono",
    min_value=3,
    max_value=12,
    value=5
)

iteraciones = st.sidebar.select_slider(
    "Cantidad de iteraciones",
    options=[1000, 5000, 10000, 20000, 50000],
    value=10000
)

modulo = st.sidebar.slider(
    "Radio del polígono",
    min_value=0.5,
    max_value=5.0,
    value=2.0,
    step=0.5
)

porcentaje = st.sidebar.slider(
    "Porcentaje de construcción",
    min_value=10,
    max_value=100,
    value=100,
    step=10
)

semilla = st.sidebar.number_input(
    "Semilla aleatoria",
    min_value=0,
    max_value=99999,
    value=42
)

puntos_x, puntos_y, vertx, verty = fractales(
    lados,
    iteraciones,
    modulo,
    semilla
)

cantidad = int(iteraciones * porcentaje / 100)

fig, ax = plt.subplots(figsize=(8, 8))

poligono_x = np.append(vertx, vertx[0])
poligono_y = np.append(verty, verty[0])

ax.plot(
    poligono_x,
    poligono_y,
    color="gray",
    linewidth=1.2,
    alpha=0.7
)

ax.scatter(
    puntos_x[:cantidad],
    puntos_y[:cantidad],
    s=2,
    color="purple",
    alpha=0.65
)

ax.scatter(
    vertx,
    verty,
    color="red",
    s=35,
    zorder=3
)

ax.scatter(
    [0],
    [0],
    color="green",
    s=35,
    zorder=3
)

ax.set_aspect("equal")
ax.set_title("Construcción del fractal")
ax.grid(alpha=0.2)

margen = modulo * 1.15
ax.set_xlim(-margen, margen)
ax.set_ylim(-margen, margen)

st.pyplot(fig, use_container_width=True)
plt.close(fig)

col1, col2, col3 = st.columns(3)

col1.metric("Lados", lados)
col2.metric("Iteraciones totales", f"{iteraciones:,}")
col3.metric("Puntos representados", f"{cantidad:,}")

st.divider()

st.markdown(
    """
    ### Experimentá

    - Cambiá la cantidad de lados y observá las diferencias.
    - Aumentá las iteraciones para descubrir cómo se define la figura.
    - Modificá el porcentaje para observar distintas etapas.
    - Cambiá la semilla aleatoria para obtener otra distribución de puntos.

    **Pregunta para investigar:** ¿Qué relación existe entre la cantidad
    de lados del polígono y la figura fractal que se obtiene?
    """
)

st.caption("Proyecto educativo de programación y geometría.")
