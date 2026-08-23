import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Resolutor de Sistemas de Ecuaciones Lineales",
    page_icon="🧮",
    layout="wide",
)

# Estilos visuales
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">🧮 Resolutor de Sistemas de Ecuaciones Lineales (Ax = b)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Aplicación interactiva basada en el Teorema de Rouché-Frobenius</div>',
    unsafe_allow_html=True,
)

with st.expander("📖 **Ver fundamento teórico (Teorema de Rouché-Frobenius)**"):
  st.markdown("""
    Dado un sistema de ecuaciones $A x = b$:
    - **Sistema Compatible Determinado (Solución Única):** $\text{rango}(A) = \text{rango}(A|b) = n$ (número de incógnitas)
    - **Sistema Compatible Indeterminado (Infinitas Soluciones):** $\text{rango}(A) = \text{rango}(A|b) < n$
    - **Sistema Incompatible (Sin Solución):** $\text{rango}(A) < \text{rango}(A|b)$
    """)

# Panel lateral de configuración
st.sidebar.header("⚙️ Configuración del Sistema")

example_choice = st.sidebar.selectbox(
    "Cargar un ejemplo predeterminado:",
    [
        "Personalizado",
        "Solución Única (2x2)",
        "Infinitas Soluciones (2x3)",
        "Sin Solución (2x2)",
    ],
)

# Valores por defecto según el ejemplo
if example_choice == "Solución Única (2x2)":
  default_rows, default_cols = 2, 2
  default_A = [[2.0, 1.0], [1.0, 3.0]]
  default_b = [[5.0], [10.0]]
elif example_choice == "Infinitas Soluciones (2x3)":
  default_rows, default_cols = 2, 3
  default_A = [[1.0, 2.0, -1.0], [2.0, 4.0, -2.0]]
  default_b = [[3.0], [6.0]]
elif example_choice == "Sin Solución (2x2)":
  default_rows, default_cols = 2, 2
  default_A = [[1.0, 1.0], [1.0, 1.0]]
  default_b = [[2.0], [5.0]]
else:
  default_rows, default_cols = 2, 2
  default_A = [[2.0, 1.0], [1.0, 3.0]]
  default_b = [[5.0], [10.0]]

rows = st.sidebar.number_input(
    "Número de filas (m)",
    min_value=1,
    max_value=10,
    value=default_rows,
    key="rows_input",
)
cols = st.sidebar.number_input(
    "Número de columnas / incógnitas (n)",
    min_value=1,
    max_value=10,
    value=default_cols,
    key="cols_input",
)

st.write("### 📝 Ingreso de la Matriz $A$ y el Vector $b$")

col_a, col_b = st.columns([3, 1.2])

with col_a:
  st.subheader("Matriz $A$")
  df_A_init = pd.DataFrame(
      (
          default_A
          if (
              example_choice != "Personalizado"
              and len(default_A) == rows
              and len(default_A[0]) == cols
          )
          else np.zeros((rows, cols))
      ),
      columns=[f"x_{i+1}" for i in range(cols)],
  )
  edited_A = st.data_editor(
      df_A_init, key="editor_A", use_container_width=True
  )

with col_b:
  st.subheader("Vector $b$")
  df_b_init = pd.DataFrame(
      (
          default_b
          if (
              example_choice != "Personalizado" and len(default_b) == rows
          )
          else np.zeros((rows, 1))
      ),
      columns=["Término Indep. (b)"],
  )
  edited_b = st.data_editor(
      df_b_init, key="editor_b", use_container_width=True
  )

if st.button(
    "🚀 Calcular y Resolver Sistema", type="primary", use_container_width=True
):
  try:
    A = edited_A.to_numpy(dtype=float)
    b = edited_b.to_numpy(dtype=float).flatten()

    # Cálculo de rangos
    rank_A = int(np.linalg.matrix_rank(A))
    n_unknowns = int(A.shape[1])
    b_reshaped = b.reshape(-1, 1)
    augmented_matrix = np.hstack((A, b_reshaped))
    rank_Ab = int(np.linalg.matrix_rank(augmented_matrix))

    st.divider()
    st.write("### 📊 Resultados del Análisis")

    m1, m2, m3 = st.columns(3)
    m1.metric("Rango de A", rank_A)
    m2.metric("Rango de [A|b]", rank_Ab)
    m3.metric("Nº Incógnitas (n)", n_unknowns)

    st.subheader("Clasificación del Sistema")

    if rank_A == rank_Ab:
      if rank_A == n_unknowns:
        st.success("✅ **Sistema Compatible Determinado (Solución Única)**")
        x = np.linalg.solve(A, b)

        st.write("#### 🎯 Solución:")
        res_df = pd.DataFrame({
            "Incógnita": [f"x_{i+1}" for i in range(len(x))],
            "Valor": [f"{val:.4f}" for val in x],
        })
        st.table(res_df)
      else:
        st.warning(
            "⚠️ **Sistema Compatible Indeterminado (Infinitas Soluciones)**"
        )
        x = np.linalg.lstsq(A, b, rcond=None)[0]

        st.write("#### 🎯 Una solución particular:")
        res_df = pd.DataFrame({
            "Incógnita": [f"x_{i+1}" for i in range(len(x))],
            "Valor Particular": [f"{val:.4f}" for val in x],
        })
        st.table(res_df)
    else:
      st.error("❌ **Sistema Incompatible (Sin Solución)**")
      st.info(
          "El rango de la matriz aumentada es mayor que el rango de A. No"
          " existen valores que satisfagan todas las ecuaciones"
          " simultáneamente."
      )

  except Exception as e:
    st.error(f"Error en los datos ingresados: {str(e)}")
