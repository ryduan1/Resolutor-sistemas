import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Resolutor de Reticulados - Método de los Nodos",
    page_icon="🏗️",
    layout="wide",
)

# Estilos visuales + Ocultar barra superior / GitHub / Menú
st.markdown(
    """
<style>
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">🏗️ Solver de Reticulados: Equilibrio de Nodos'
    ' [A]x = b</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Análisis de Estabilidad y Resolución de Fuerzas'
    ' Internas y Reacciones</div>',
    unsafe_allow_html=True,
)

# --- TEORÍA DE RETICULADOS ---
with st.expander(
    "📖 **Ver Fundamento Teórico y Clasificación de Equilibrio**", expanded=False
):
  st.markdown("""
    ### Recordemos: $[A] x = b$
    En el método de los nodos para reticulados planos:
    - **$[A]$**: Matriz de coeficientes directores de las barras y componentes de reacciones en cada nodo.
    - **$x$**: Vector de incógnitas (Fuerzas internas de barras $B_{ij}$ y Reacciones de apoyo $R_k$).
    - **$b$**: Vector de cargas externas aplicadas en los nodos ($\Sigma F_x$, $\Sigma F_y$).
    
    ---
    
    ### Criterio de Rouché-Frobenius Aplicado a Estructuras:
    
    | Condición Matemática | Condición Estructural | Estado de Equilibrio |
    | :--- | :--- | :--- |
    | **$\text{Rango}(A) = \text{Rango}(A:b) = n$** | **Solución Única** | **LOGRA EL EQUILIBRIO** (Estructura Isostática) |
    | **$\text{Rango}(A) = \text{Rango}(A:b) < n$** | **Infinitas soluciones** | **LOGRA EL EQUILIBRIO** (Estructura Hiperestática) |
    | **$\text{Rango}(A) \\neq \text{Rango}(A:b)$** | **No existe solución** | **NO LOGRA EL EQUILIBRIO** (Mecanismo / Hipostática) |
    
    - **Sistema Compatible:** Un sistema es compatible cuando **se puede lograr el equilibrio**.
    - **Sistema Incompatible:** Un sistema es incompatible cuando **no es posible lograr el equilibrio**.
    """)

# --- CHECKBOX DE EJEMPLO DE LA CÁTEDRA (PRIMERO) ---
cargar_ejemplo = st.checkbox(
    "📌 Cargar ejemplo teórico de la cátedra (6 nodos, 9 barras, 3 reacciones)"
)

# Definir valores por defecto según el checkbox
if cargar_ejemplo:
  default_nodos = 6
  default_barras = "B12, B23, B34, B45, B56, B16, B15, B25, B35"
  default_reacciones = "R1, R4x, R4y"
else:
  default_nodos = 3
  default_barras = "B12, B23, B13"
  default_reacciones = "R1x, R1y, R2"

# --- CONFIGURACIÓN DEL RETICULADO EN BARRA LATERAL ---
st.sidebar.header("⚙️ Configuración del Reticulado")

num_nodos = st.sidebar.number_input(
    "Número de Nodos (N)",
    min_value=1,
    max_value=50,
    value=default_nodos,
    step=1,
)

barras_str = st.sidebar.text_input(
    "Nombres de Barras (separadas por comas):", value=default_barras
)
reacciones_str = st.sidebar.text_input(
    "Nombres de Reacciones (separadas por comas):", value=default_reacciones
)

# Procesar nombres de variables
barras = [b.strip() for b in barras_str.split(",") if b.strip()]
reacciones = [r.strip() for r in reacciones_str.split(",") if r.strip()]

b_count = len(barras)
r_count = len(reacciones)
max_barras_posibles = (
    int(num_nodos * (num_nodos - 1) / 2) if num_nodos >= 2 else 0
)

# --- VALIDACIONES DE REGLAS ESTRUCTURALES ---
st.sidebar.divider()
st.sidebar.subheader("📐 Validaciones Geométricas")

if num_nodos < 2:
  st.sidebar.error("❌ Un reticulado requiere al menos 2 nodos para existir.")
elif b_count > max_barras_posibles:
  st.sidebar.warning(
      f"⚠️ Para {num_nodos} nodos, el máximo geométrico de barras sin duplicar"
      f" es {max_barras_posibles}."
  )
else:
  grado_libertad = (b_count + r_count) - (2 * num_nodos)
  st.sidebar.write(f"**Ecuaciones ($2N$):** {2*num_nodos}")
  st.sidebar.write(f"**Incógnitas ($b+r$):** {b_count + r_count}")

  if grado_libertad < 0:
    st.sidebar.error(
        f"🔴 **b + r < 2N** (Hipostático / Mecanismo)\nFaltan"
        f" {abs(grado_libertad)} elemento(s) para estabilidad."
    )
  elif grado_libertad == 0:
    st.sidebar.success(
        "🟢 **b + r = 2N**\nCumple la condición necesaria de Isostaticidad."
    )
  else:
    st.sidebar.info(
        f"🔵 **b + r > 2N** (Hiperestático)\nTiene {grado_libertad} elemento(s)"
        " redundante(s)."
    )

# Columnas e Index para DataFrames
columnas_x = barras + reacciones
num_incognitas = len(columnas_x)

filas_eq = []
for i in range(1, num_nodos + 1):
  filas_eq.append(f"Nodo {i} - ΣFx")
  filas_eq.append(f"Nodo {i} - ΣFy")

num_ecuaciones = len(filas_eq)

st.write("### 📝 Sistema de Ecuaciones del Reticulado")
st.write(
    f"**Ecuaciones totales:** {num_ecuaciones} ({num_nodos} nodos × 2 ejes) |"
    f" **Incógnitas totales:** {num_incognitas} ({b_count} barras + {r_count}"
    " reacciones)"
)

# Carga de datos de la matriz según el estado del checkbox
if cargar_ejemplo and num_nodos == 6 and num_incognitas == 12:
  default_A_data = [
      [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7071, 0.0, 0.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.7071, 0.0, 0.0, 1.0, 0.0, 0.0],
      [-1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
      [0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.7071, 0.0, 0.0, 0.0],
      [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.7071, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
      [0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
      [0.0, 0.0, 0.0, 1.0, -1.0, 0.0, -0.7071, 0.0, 0.7071, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.7071, -1.0, -0.7071, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [0.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
  ]
  default_b_data = [0, 0, 0, 16, 0, 0, 0, 0, 0, 0, -12, 0]
  df_A_init = pd.DataFrame(default_A_data, index=filas_eq, columns=columnas_x)
  df_b_init = pd.DataFrame(
      default_b_data, index=filas_eq, columns=["Cargas Ext. (b)"]
  )
else:
  df_A_init = pd.DataFrame(
      np.zeros((num_ecuaciones, num_incognitas)),
      index=filas_eq,
      columns=columnas_x,
  )
  df_b_init = pd.DataFrame(
      np.zeros((num_ecuaciones, 1)), index=filas_eq, columns=["Cargas Ext. (b)"]
  )

col_mat_A, col_vec_b = st.columns([3.5, 1.2])

with col_mat_A:
  st.subheader("Matriz de Coeficientes $[A]$")
  edited_A = st.data_editor(
      df_A_init, key="editor_A_reticulados", use_container_width=True
  )

with col_vec_b:
  st.subheader("Vector de Cargas $[b]$")
  edited_b = st.data_editor(
      df_b_init, key="editor_b_reticulados", use_container_width=True
  )

# --- BOTÓN DE CÁLCULO Y DIAGNÓSTICO ---
if st.button(
    "🚀 Resolver Equilibrio del Reticulado",
    type="primary",
    use_container_width=True,
):
  try:
    A = edited_A.to_numpy(dtype=float)
    b = edited_b.to_numpy(dtype=float).flatten()

    rank_A = int(np.linalg.matrix_rank(A))
    n_unknowns = A.shape[1]
    b_reshaped = b.reshape(-1, 1)
    augmented_matrix = np.hstack((A, b_reshaped))
    rank_Ab = int(np.linalg.matrix_rank(augmented_matrix))

    st.divider()
    st.write("### 📊 Resultados del Análisis Estructural")

    c_rA, c_rAb, c_n = st.columns(3)
    c_rA.metric("Rango de [A]", rank_A)
    c_rAb.metric("Rango de [A:b]", rank_Ab)
    c_n.metric("Nº Incógnitas (n)", n_unknowns)

    st.subheader("Estado de Equilibrio del Sistema")

    if rank_A == rank_Ab:
      if rank_A == n_unknowns:
        st.success(
            "✅ **LOGRA EL EQUILIBRIO - Solución Única (Sistema Isostático)**"
        )
        st.write(
            "El reticulado es estable e isostático. Existe un único conjunto"
            " de fuerzas internas y reacciones que garantizan el equilibrio."
        )

        x = np.linalg.solve(A, b)

        res_df = pd.DataFrame({
            "Incógnita / Componente": columnas_x,
            "Tipo": [
                "Fuerza en Barra" if col in barras else "Reacción de Apoyo"
                for col in columnas_x
            ],
            "Valor Calculado": [f"{val:.4f}" for val in x],
        })

        st.write("#### 🎯 Resultados de Fuerzas Internas y Reacciones:")
        st.table(res_df)

      else:
        st.warning(
            "⚠️ **LOGRA EL EQUILIBRIO - Infinitas Soluciones (Sistema"
            " Hiperestático)**"
        )
        st.write(
            "El reticulado es hiperestático. Posee más incógnitas que"
            " ecuaciones de equilibrio independientes."
        )

        x = np.linalg.lstsq(A, b, rcond=None)[0]

        res_df = pd.DataFrame({
            "Incógnita / Componente": columnas_x,
            "Solución Particular": [f"{val:.4f}" for val in x],
        })
        st.write("#### 🎯 Solución Particular (Mínimos Cuadrados):")
        st.table(res_df)
    else:
      st.error(
          "❌ **NO LOGRA EL EQUILIBRIO - Sin Solución (Sistema Incompatible)**"
      )
      st.write(
          "El sistema es **incompatible / hipostático (mecanismo)**. Las"
          " cargas externas aplicadas no pueden ser equilibradas por la"
          " disposición de barras y apoyos actual."
      )

  except Exception as e:
    st.error(f"Error en los cálculos: {str(e)}")
