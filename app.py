import base64
import numpy as np
import pandas as pd
import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Solver de Reticulados | Facultad de Ingeniería UNRC",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Logo oficial UNRC en Base64 (autocontenido)
LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAA3EAAANoCAYAAACpW39XAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAIABJREFUeJzs3Xd4VGX2A/DvPVPSSaY3QpLQTXoRREREAUVBXdfu2mvdXddf..."  # [String truncado en vista, se genera completo en tu app.py]

# --- ESTILOS CSS PROFESIONALES (TEMA INGENIERÍA) ---
st.markdown(
    """
    <style>
        /* Ocultar menú principal, footer y botones de Deploy/GitHub */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        [data-testid="stAppDeployButton"] { display: none !important; }
        [data-testid="stToolbarActions"] { display: none !important; }
        /* Hacer el header transparente para que no moleste visualmente pero mantenga activa la sidebar */
        header[data-testid="stHeader"] {
        background: transparent !important;
        }
        
        /* Paleta de colores y fuentes */
        .main-header {
            font-size: 2.1rem;
            color: #4A90E2;
            font-weight: 800;
            margin-bottom: 0.1rem;
            letter-spacing: -0.5px;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #475569;
            margin-bottom: 1.2rem;
            font-weight: 500;
        }
        .institution-badge {
            font-size: 0.85rem;
            font-weight: 700;
            color: #1E40AF;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.3rem;
        }
        
        /* Pie de página institucional */
        .custom-footer {
            background-color: #0F172A;
            color: #94A3B8;
            text-align: center;
            padding: 20px 10px;
            font-size: 0.88rem;
            border-radius: 8px;
            margin-top: 50px;
            line-height: 1.6;
        }
        .custom-footer b { color: #F8FAFC; }
        .custom-footer a { color: #60A5FA; text-decoration: none; }
        .custom-footer a:hover { text-decoration: underline; }
        
        /* Alineación del logo en sidebar */
        .sidebar-logo-container {
            text-align: center;
            padding-bottom: 15px;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 15px;
        }
        .sidebar-logo-container img {
            max-width: 130px;
            height: auto;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# --- CABECERA PRINCIPAL CON LOGO INSTITUCIONAL ---
col_logo_head, col_title_head = st.columns([0.8, 4.2])

with col_logo_head:
  st.markdown(
      '<div style="text-align: center; padding-top: 5px;"><img'
      f' src="data:image/png;base64,{LOGO_B64}" style="max-height: 90px; width:'
      ' auto;"></div>',
      unsafe_allow_html=True,
  )

with col_title_head:
  st.markdown(
      '<div class="institution-badge">Universidad Nacional de Río Cuarto —'
      ' Facultad de Ingeniería</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="main-header">🏗️ Solver de Reticulados: Equilibrio de Nodos'
      ' [A]x = b</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<div class="sub-header">Plataforma para el Análisis de Estabilidad y'
      ' Resolución de Fuerzas Internas y Reacciones en Estructuras'
      ' Planas</div>',
      unsafe_allow_html=True,
  )

# --- FUNDAMENTO TEÓRICO Y ROUCHÉ-FROBENIUS ---
with st.expander(
    "📖 **Fundamento Teórico: Método de los Nodos y Criterios de Equilibrio**",
    expanded=False,
):
  st.markdown("""
    ### Planteo Matricial: $[A] x = b$
    En el método de los nodos para reticulados planos articulados:
    - **$[A]$**: Matriz de coeficientes directores de barras y componentes de reacción por nodo.
    - **$x$**: Vector de incógnitas que contiene las Fuerzas Internas en barras ($B_{ij}$) y Reacciones de apoyo ($R_k$).
    - **$b$**: Vector de cargas externas aplicadas en los nodos ($\Sigma F_x$, $\Sigma F_y$).
    
    ---
    
    ### Clasificación de Equilibrio según Rouché-Frobenius:
    
    | Condición Matemática | Clasificación Estructural | Estado de Equilibrio |
    | :--- | :--- | :--- |
    | **$\text{Rango}(A) = \text{Rango}(A:b) = n$** | **Compatible Determinado** | **LOGRA EL EQUILIBRIO** (Estructura Isostática — Solución Única) |
    | **$\text{Rango}(A) = \text{Rango}(A:b) < n$** | **Compatible Indeterminado** | **LOGRA EL EQUILIBRIO** (Estructura Hiperestática — Infinitas Soluciones) |
    | **$\text{Rango}(A) \\neq \text{Rango}(A:b)$** | **Incompatible** | **NO LOGRA EL EQUILIBRIO** (Mecanismo / Estructura Hipostática) |
    
    * **Sistema Compatible:** Se logra el equilibrio estático de la estructura.
    * **Sistema Incompatible:** No es posible alcanzar el equilibrio estático con la configuración actual.
    """)

# --- BARRA LATERAL (CONFIGURACIÓN Y LOGO) ---
st.sidebar.markdown(
    f'<div class="sidebar-logo-container"><img'
    f' src="data:image/png;base64,{LOGO_B64}"><div style="font-size: 0.85rem;'
    ' font-weight: 700; color: #1E40AF; margin-top: 8px;">FACULTAD DE'
    ' INGENIERÍA</div><div style="font-size: 0.75rem; color:'
    ' #64748B;">UNRC</div></div>',
    unsafe_allow_html=True,
)

st.sidebar.header("⚙️ Configuración del Reticulado")

# Cargar Ejemplo Teórico de Cátedra
cargar_ejemplo = st.checkbox(
    "📌 Cargar ejemplo teórico de la cátedra (6 nodos, 9 barras, 3 reacciones)"
)

if cargar_ejemplo:
  default_nodos = 6
  default_barras = "B12, B23, B34, B45, B56, B16, B15, B25, B35"
  default_reacciones = "R1, R4x, R4y"
else:
  default_nodos = 3
  default_barras = "B12, B23, B13"
  default_reacciones = "R1x, R1y, R2"

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

barras = [b.strip() for b in barras_str.split(",") if b.strip()]
reacciones = [r.strip() for r in reacciones_str.split(",") if r.strip()]

b_count = len(barras)
r_count = len(reacciones)
max_barras_posibles = (
    int(num_nodos * (num_nodos - 1) / 2) if num_nodos >= 2 else 0
)

# Validaciones geométricas
st.sidebar.divider()
st.sidebar.subheader("📐 Validaciones Geométricas")

if num_nodos < 2:
  st.sidebar.error("❌ Un reticulado requiere al menos 2 nodos para configurarse.")
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
        f" {abs(grado_libertad)} elemento(s) para la estabilidad preliminar."
    )
  elif grado_libertad == 0:
    st.sidebar.success(
        "🟢 **b + r = 2N**\nCumple la condición necesaria de Isostaticidad."
    )
  else:
    st.sidebar.info(
        f"🔵 **b + r > 2N** (Hiperestático)\nPosee {grado_libertad} elemento(s)"
        " redundante(s)."
    )

columnas_x = barras + reacciones
num_incognitas = len(columnas_x)

filas_eq = []
for i in range(1, num_nodos + 1):
  filas_eq.append(f"Nodo {i} - ΣFx")
  filas_eq.append(f"Nodo {i} - ΣFy")

num_ecuaciones = len(filas_eq)

st.write("### 📝 Sistema de Ecuaciones de Equilibrio Nodal")
st.write(
    f"**Ecuaciones planteadas:** {num_ecuaciones} ({num_nodos} nodos × 2 ejes) |"
    f" **Incógnitas:** {num_incognitas} ({b_count} barras + {r_count}"
    " reacciones)"
)

# Matriz e Inicialización
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
  st.subheader("Vector de Cargas Nodales $[b]$")
  edited_b = st.data_editor(
      df_b_init, key="editor_b_reticulados", use_container_width=True
  )

# --- BOTÓN DE RESOLUCIÓN Y EVALUACIÓN ---
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
    st.write("### 📊 Diagnóstico y Resultados de Análisis Estructural")

    c_rA, c_rAb, c_n = st.columns(3)
    c_rA.metric("Rango de [A]", rank_A)
    c_rAb.metric("Rango de [A:b]", rank_Ab)
    c_n.metric("Nº Incógnitas (n)", n_unknowns)

    st.subheader("Estado de Equilibrio de la Estructura")

    if rank_A == rank_Ab:
      if rank_A == n_unknowns:
        st.success(
            "✅ **LOGRA EL EQUILIBRIO — Solución Única (Sistema Isostático)**"
        )
        st.write(
            "El reticulado es **isostático y estable**. Existe una única"
            " combinación de fuerzas internas y reacciones capaz de equilibrar"
            " la estructura."
        )

        x = np.linalg.solve(A, b)

        res_df = pd.DataFrame({
            "Incógnita / Componente": columnas_x,
            "Tipo de Elemento": [
                "Fuerza en Barra" if col in barras else "Reacción de Apoyo"
                for col in columnas_x
            ],
            "Valor Calculado": [f"{val:.4f}" for val in x],
            "Estado / Solicitación": [
                "Tracción (+)"
                if val > 0.0001
                else ("Compresión (-)" if val < -0.0001 else "Barra Nula / Neutra")
                for val in x
            ],
        })

        st.write("#### 🎯 Solución del Vector Incógnita $x$:")
        st.table(res_df)

      else:
        st.warning(
            "⚠️ **LOGRA EL EQUILIBRIO — Infinitas Soluciones (Sistema"
            " Hiperestático)**"
        )
        st.write(
            "La estructura es **hiperestática**. Cuenta con elementos"
            " redundantes y requiere ecuaciones de compatibilidad de"
            " deformaciones para una solución única."
        )

        x = np.linalg.lstsq(A, b, rcond=None)[0]

        res_df = pd.DataFrame({
            "Incógnita / Componente": columnas_x,
            "Tipo de Elemento": [
                "Fuerza en Barra" if col in barras else "Reacción de Apoyo"
                for col in columnas_x
            ],
            "Solución Particular (Mín. Cuadrados)": [f"{val:.4f}" for val in x],
        })
        st.write("#### 🎯 Solución Particular Calculada:")
        st.table(res_df)
    else:
      st.error(
          "❌ **NO LOGRA EL EQUILIBRIO — Sin Solución (Sistema Incompatible /"
          " Hipostático)**"
      )
      st.write(
          "La estructura constituye un **mecanismo inestable**. Las cargas"
          " aplicadas no pueden ser soportadas por la disposición actual de"
          " barras y apoyos."
      )

  except Exception as e:
    st.error(f"Error en el procesamiento de datos: {str(e)}")

# --- PIE DE PÁGINA INSTITUCIONAL Y AUTORÍA ---
st.markdown(
    """
    <div class="custom-footer">
        <b>Desarrollado para la Cátedra de Estructuras / Mecánica del Continuo</b><br>
        Facultad de Ingeniería — Universidad Nacional de Río Cuarto (UNRC)<br><br>
        <b>Autor:</b> Estudiante de Ingeniería Ryduan Maximiliano Arévalo Castellano<br>
        <b>Contacto:</b> <a href="mailto:ryduare@gmail.com">ryduare@gmail.com</a>
    </div>
""",
    unsafe_allow_html=True,
)
