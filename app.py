import time
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Solver de Matrices ´n´ incognitas",
    page_icon="🧮",
    layout="wide",
)

st.markdown(
    """
<style>
    .main-header { font-size: 2.2rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0.2rem; }
    .sub-header { font-size: 1.1rem; color: #4B5563; margin-bottom: 1.5rem; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="main-header">🧮 Solver de Matrices ´n´ incognitas (Ax = b)</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Soporta desde sistemas pequeños hasta matrices gigantes (ej. 500x500)</div>',
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.header("⚙️ Modo de Ingreso de Datos")
modo_ingreso = st.sidebar.radio(
    "Selecciona cómo ingresar el sistema:",
    [
        "📊 Tabla Interactiva (Sistemas pequeños)",
        "📝 Pegar Texto (Espacios / Comas)",
        "📁 Subir Archivo CSV",
        "🎲 Generador Aleatorio (Prueba de rendimiento)",
    ],
)

A = None
b = None

# -------------------------------------------------------------
# MODO 1: TABLA INTERACTIVA
# -------------------------------------------------------------
if modo_ingreso == "📊 Tabla Interactiva (Sistemas pequeños)":
  st.subheader("Ingreso mediante Tabla")
  c1, c2 = st.columns(2)
  rows = c1.number_input("Número de filas (m)", min_value=1, value=2, step=1)
  cols = c2.number_input(
      "Número de columnas / incógnitas (n)", min_value=1, value=2, step=1
  )

  col_a, col_b = st.columns([3, 1.2])
  with col_a:
    st.write("**Matriz A**")
    df_A = pd.DataFrame(
        np.zeros((rows, cols)), columns=[f"x_{i+1}" for i in range(cols)]
    )
    edited_A = st.data_editor(df_A, key="editor_A", use_container_width=True)
    A = edited_A.to_numpy(dtype=float)

  with col_b:
    st.write("**Vector b**")
    df_b = pd.DataFrame(np.zeros((rows, 1)), columns=["Término Indep. (b)"])
    edited_b = st.data_editor(df_b, key="editor_b", use_container_width=True)
    b = edited_b.to_numpy(dtype=float).flatten()

# -------------------------------------------------------------
# MODO 2: PEGAR TEXTO (Fiel a tu Colab original)
# -------------------------------------------------------------
elif modo_ingreso == "📝 Pegar Texto (Espacios / Comas)":
  st.subheader("Ingreso por Bloque de Texto")
  st.write(
      "Ingresa una fila por línea. Separa los elementos de cada fila con"
      " espacios o comas."
  )

  text_A = st.text_area(
      "Elementos de la Matriz A (Fila por fila):",
      value="2 1\n1 3",
      height=150,
  )
  text_b = st.text_area(
      "Elementos del Vector b (Separados por espacio o línea por línea):",
      value="5 10",
      height=80,
  )

  if text_A and text_b:
    try:
      # Parse A
      lines_A = text_A.strip().split("\n")
      matrix_a = []
      for line in lines_A:
        clean_line = line.replace(",", " ").split()
        if clean_line:
          matrix_a.append([float(val) for val in clean_line])
      A = np.array(matrix_a)

      # Parse b
      clean_b = text_b.replace(",", " ").replace("\n", " ").split()
      b = np.array([float(val) for val in clean_b])

      st.info(
          f" Matriz A detectada de dimensión: **{A.shape[0]} x {A.shape[1]}**"
          f" | Vector b de longitud: **{len(b)}**"
      )
    except Exception as e:
      st.error(f"Error al procesar el texto: {str(e)}")

# -------------------------------------------------------------
# MODO 3: SUBIR ARCHIVO CSV
# -------------------------------------------------------------
elif modo_ingreso == "📁 Subir Archivo CSV":
  st.subheader("Cargar Matrices desde Archivos CSV")
  file_A = st.file_uploader(
      "Subir Matriz A (CSV sin encabezados)", type=["csv", "txt"]
  )
  file_b = st.file_uploader(
      "Subir Vector b (CSV sin encabezados)", type=["csv", "txt"]
  )

  if file_A and file_b:
    try:
      A = pd.read_csv(file_A, header=None).to_numpy(dtype=float)
      b = pd.read_csv(file_b, header=None).to_numpy(dtype=float).flatten()
      st.success(
          f" Archivos cargados correctamente. Dimensión de A:"
          f" **{A.shape[0]}x{A.shape[1]}**"
      )
    except Exception as e:
      st.error(f"Error al leer los archivos: {str(e)}")

# -------------------------------------------------------------
# MODO 4: GENERADOR ALEATORIO (Para matrices gigantes 500x500)
# -------------------------------------------------------------
elif modo_ingreso == "🎲 Generador Aleatorio (Prueba de rendimiento)":
  st.subheader("Generador de Matrices Gigantes")
  st.write(
      "Prueba la capacidad del sistema para resolver matrices de gran escala"
      " (ej. 100x100, 500x500)."
  )

  dim = st.number_input(
      "Tamaño de la matriz cuadrada (N x N)",
      min_value=2,
      max_value=2000,
      value=500,
      step=50,
  )

  if st.button("🎲 Generar Matriz Aleatoria"):
    with st.spinner(f"Generando matriz de {dim} x {dim}..."):
      st.session_state["A_gen"] = np.random.uniform(-10, 10, size=(dim, dim))
      st.session_state["b_gen"] = np.random.uniform(-10, 10, size=dim)

  if "A_gen" in st.session_state and st.session_state["A_gen"].shape[0] == dim:
    A = st.session_state["A_gen"]
    b = st.session_state["b_gen"]
    st.info(f" Matriz generada de **{dim} x {dim}** ({dim*dim:,} elementos).")

# -------------------------------------------------------------
# RESOLUCIÓN Y ANÁLISIS DEL SISTEMA
# -------------------------------------------------------------
if A is not None and b is not None:
  st.divider()

  if A.shape[0] != len(b):
    st.error(
        f"❌ **Error de dimensiones:** El número de filas de A ({A.shape[0]})"
        f" no coincide con el tamaño del vector b ({len(b)})."
    )
  else:
    if st.button(
        "🚀 Calcular y Resolver Sistema", type="primary", use_container_width=True
    ):
      start_time = time.time()

      # Cálculo de rangos
      rank_A = int(np.linalg.matrix_rank(A))
      n_unknowns = int(A.shape[1])
      b_reshaped = b.reshape(-1, 1)
      augmented_matrix = np.hstack((A, b_reshaped))
      rank_Ab = int(np.linalg.matrix_rank(augmented_matrix))

      exec_time = time.time() - start_time

      st.write("### 📊 Resultados del Análisis")

      m1, m2, m3, m4 = st.columns(4)
      m1.metric("Rango de A", rank_A)
      m2.metric("Rango de [A|b]", rank_Ab)
      m3.metric("Nº Incógnitas (n)", n_unknowns)
      m4.metric("Tiempo de Cálculo", f"{exec_time:.4f} seg")

      st.subheader("Clasificación del Sistema")

      if rank_A == rank_Ab:
        if rank_A == n_unknowns:
          st.success("✅ **Sistema Compatible Determinado (Solución Única)**")
          x = np.linalg.solve(A, b)

          st.write("#### 🎯 Vector Incógnita Solución (x):")
          if len(x) <= 20:
            res_df = pd.DataFrame({
                "Incógnita": [f"x_{i+1}" for i in range(len(x))],
                "Valor": [f"{val:.6f}" for val in x],
            })
            st.table(res_df)
          else:
            st.write(
                f"*(Mostrando los primeros 20 elementos de los {len(x)}"
                " totales)*"
            )
            res_df = pd.DataFrame({
                "Incógnita": [f"x_{i+1}" for i in range(20)],
                "Valor": [f"{val:.6f}" for val in x[:20]],
            })
            st.table(res_df)

            # Opción para descargar la solución completa
            csv_sol = pd.DataFrame(
                x, columns=["Solucion"]
            ).to_csv(index=False)
            st.download_button(
                "📥 Descargar Solución Completa (CSV)",
                data=csv_sol,
                file_name="solucion_x.csv",
                mime="text/csv",
            )

        else:
          st.warning(
              "⚠️ **Sistema Compatible Indeterminado (Infinitas Soluciones)**"
          )
          x = np.linalg.lstsq(A, b, rcond=None)[0]
          st.write("#### 🎯 Una solución particular:")
          st.write(x[:20] if len(x) > 20 else x)
      else:
        st.error("❌ **Sistema Incompatible (Sin Solución)**")
