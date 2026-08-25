import base64
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Solver de Reticulados | Facultad de Ingeniería UNRC",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- LOGO OFICIAL UNRC ---
LOGO_B64 = "iVBORw0KGgoAAAANSUhEUgAAAk8AAANYCAMAAADqvfnLAAAABGdBTUEAAK/INwWK6QAAABl0RVh0U29mdHdhcmUAQWRvYmUgSW1hZ2VSZWFkeXHJZTwAAAGAUExURf/z1v3v0//THPXs0/fOJyUpISIkGu3jy2KWqvbrztXLtDMzKU9QR+jex0pFNv/229eyLfPnzHBzbWewzJGIcxohF/vtzxQYFLSqljc5MK6RMyowKEQ5L9JnZW1nV3FKRv9tbY1QTfr598i7pWvj/wgVFP9xcRsnJGrH6VdrcCg1MY53NKhZV//cHWJVN97WwZmSgTxAN2Xb/4R7aORqabuzoO/n0HVkMy4sJKediGvW/PXnxyAbFFx8iHHb/7plYwEICj5GQn9xW2vN8v9tcbdgXQcRDvVtbWvT9/txb1xeVcZjYQYMDtacaxIUDy0oHbRcXSAtLU1cXWu/33HH5vfv2H1/eGTW/V4+PMJdW+9zcvPn0+1tbfvv1zIwH+pybhEcG//74TotLWnb/ykuHm3b/8NfZDI8OWXT9//jG2FOJSAeH5hbWB8gE1hJKBAPEg4NC2nf/23f//vz2/frx23b+m7P7//fIMjCsGnb+//zz99ZW2/R7/fz16h+dv///2vPBMcAAACAdFJOU/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AOAVLZwACNXFJREFUeNrsvf9r6tgaN/pSjAgJodSR88aE/uRgVZSTDpfmyjG8TuGlCPeKtey+P4Wyk+CZGVow0JYNA/dfv8/nWSvJWkm07Z6Zc/aGWbYaNcaYfPJ5nvV8/R//39/j7/Hnjf/x9yH4e/yNp7/H33j6e/yNp7/H3+NvPP09/sbT3+NvPP09/h5/4+nv8Z/A0//8pI3Fp8XZGf99+kR/xb8cZzw+if9PtfF//xP3P4lV+fbp0w+8AbGdM32ILcvtnH2S2/2Uv8GfK14+K787fy3fYvkJuZ0PjZ/kbvzEG/oJn6fFs58+/aRvqrrZ/N2f8t+njB/kOz/8gL98rZ/El4jvoi/AF4ql8rDR/U9n4u8n7EO5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"

# --- RENDERIZADO DE LOGO Y ENCABEZADO ---
def render_header():
    sidebar_html = f"""
        <div style="text-align: center; padding: 10px;">
            <img src="data:image/png;base64,{LOGO_B64}" style="max-width: 80%; height: auto; margin-bottom: 10px;">
            <h4 style="margin:0; color: #1E3A8A;">Facultad de Ingeniería</h4>
            <p style="font-size: 0.85rem; color: #4B5563;">UNRC | Estructuras I / Mecánica</p>
        </div>
        <hr style="margin-top: 5px; margin-bottom: 15px;">
    """
    st.sidebar.markdown(sidebar_html, unsafe_allow_html=True)

render_header()

# ==============================================================================
# FUNCIONES DEL MOTOR DE CÁLCULO (MÉTODOS DE RIGIDEZ DIRECTA 2D)
# ==============================================================================

def solve_truss(nodes_df, elements_df):
    """
    Calcula desplazamientos, reacciones y fuerzas axiales para un reticulado 2D.
    """
    num_nodes = len(nodes_df)
    num_dofs = 2 * num_nodes
    
    # Matriz de Rigidez Global nula
    K_global = np.zeros((num_dofs, num_dofs))
    
    # Ensamble de la matriz global
    lengths = []
    angles = []
    
    for idx, row in elements_df.iterrows():
        ni = int(row['Nodo i']) - 1
        nj = int(row['Nodo j']) - 1
        E = float(row['E [GPa]']) * 1e9  # GPa a Pa
        A = float(row['A [cm2]']) * 1e-4  # cm2 a m2
        
        xi, yi = nodes_df.loc[ni, 'X [m]'], nodes_df.loc[ni, 'Y [m]']
        xj, yj = nodes_df.loc[nj, 'X [m]'], nodes_df.loc[nj, 'Y [m]']
        
        L = np.sqrt((xj - xi)**2 + (yj - yi)**2)
        c = (xj - xi) / L  # cos
        s = (yj - yi) / L  # sin
        
        lengths.append(L)
        angles.append(np.arctan2(yj - yi, xj - xi))
        
        # Matriz de rigidez local en coordenadas globales
        k_coeff = (E * A) / L
        k_local = k_coeff * np.array([
            [ c*c,  c*s, -c*c, -c*s],
            [ c*s,  s*s, -c*s, -s*s],
            [-c*c, -c*s,  c*c,  c*s],
            [-c*s, -s*s,  c*s,  s*s]
        ])
        
        # Grados de libertad asociados
        dofs = [2*ni, 2*ni+1, 2*nj, 2*nj+1]
        
        for i_l in range(4):
            for j_l in range(4):
                K_global[dofs[i_l], dofs[j_l]] += k_local[i_l, j_l]
                
    # Vector de cargas externas
    F = np.zeros(num_dofs)
    fixed_dofs = []
    
    for idx, row in nodes_df.iterrows():
        n = int(row['Nodo']) - 1
        F[2*n] = float(row['Fx [kN]']) * 1000.0  # kN a N
        F[2*n+1] = float(row['Fy [kN]']) * 1000.0
        
        support = str(row['Apoyo']).strip().lower()
        if support in ['fijo', 'pin']:
            fixed_dofs.extend([2*n, 2*n+1])
        elif support in ['móvil x', 'movil x', 'roller x']:
            fixed_dofs.append(2*n+1)  # Restringe Y
        elif support in ['móvil y', 'movil y', 'roller y']:
            fixed_dofs.append(2*n)    # Restringe X

    fixed_dofs = list(set(fixed_dofs))
    free_dofs = [dof for dof in range(num_dofs) if dof not in fixed_dofs]
    
    # Reducción de matriz para resolver desplazamientos
    K_free = K_global[np.ix_(free_dofs, free_dofs)]
    F_free = F[free_dofs]
    
    U = np.zeros(num_dofs)
    try:
        U_free = np.linalg.solve(K_free, F_free)
        U[free_dofs] = U_free
    except np.linalg.LinAlgError:
        return None, "La estructura es mecanicismo (inestable) o faltan apoyos suficientes."

    # Reacciones en apoyos
    R = K_global @ U - F

    # Esfuerzos axiales en cada barra
    axial_forces = []
    stresses = []
    
    for idx, row in elements_df.iterrows():
        ni = int(row['Nodo i']) - 1
        nj = int(row['Nodo j']) - 1
        E = float(row['E [GPa]']) * 1e9
        A = float(row['A [cm2]']) * 1e-4
        L = lengths[idx]
        
        xi, yi = nodes_df.loc[ni, 'X [m]'], nodes_df.loc[ni, 'Y [m]']
        xj, yj = nodes_df.loc[nj, 'X [m]'], nodes_df.loc[nj, 'Y [m]']
        c = (xj - xi) / L
        s = (yj - yi) / L
        
        u_elem = np.array([U[2*ni], U[2*ni+1], U[2*nj], U[2*nj+1]])
        # N = (EA/L) * [-c, -s, c, s] * u
        N = (E * A / L) * np.dot(np.array([-c, -s, c, s]), u_elem)
        axial_forces.append(N / 1000.0) # Convertir a kN
        stresses.append((N / A) / 1e6)  # Convertir a MPa

    results = {
        'U': U,
        'R': R,
        'Axial_Forces': np.array(axial_forces),
        'Stresses': np.array(stresses),
        'Lengths': np.array(lengths)
    }
    return results, None


# ==============================================================================
# EJEMPLOS PREDEFINIDOS
# ==============================================================================

def load_example(example_name):
    if example_name == "Reticulado Triangular Simple":
        nodes = pd.DataFrame([
            {'Nodo': 1, 'X [m]': 0.0, 'Y [m]': 0.0, 'Apoyo': 'Fijo', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
            {'Nodo': 2, 'X [m]': 4.0, 'Y [m]': 0.0, 'Apoyo': 'Móvil X', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
            {'Nodo': 3, 'X [m]': 2.0, 'Y [m]': 3.0, 'Apoyo': 'Libre', 'Fx [kN]': 10.0, 'Fy [kN]': -25.0},
        ])
        elements = pd.DataFrame([
            {'Barra': 1, 'Nodo i': 1, 'Nodo j': 2, 'E [GPa]': 210.0, 'A [cm2]': 15.0},
            {'Barra': 2, 'Nodo i': 1, 'Nodo j': 3, 'E [GPa]': 210.0, 'A [cm2]': 15.0},
            {'Barra': 3, 'Nodo i': 2, 'Nodo j': 3, 'E [GPa]': 210.0, 'A [cm2]': 15.0},
        ])
    elif example_name == "Cercha Pratt (6 Nodos)":
        nodes = pd.DataFrame([
            {'Nodo': 1, 'X [m]': 0.0, 'Y [m]': 0.0, 'Apoyo': 'Fijo', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
            {'Nodo': 2, 'X [m]': 3.0, 'Y [m]': 0.0, 'Apoyo': 'Libre', 'Fx [kN]': 0.0, 'Fy [kN]': -30.0},
            {'Nodo': 3, 'X [m]': 6.0, 'Y [m]': 0.0, 'Apoyo': 'Móvil X', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
            {'Nodo': 4, 'X [m]': 0.0, 'Y [m]': 2.0, 'Apoyo': 'Libre', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
            {'Nodo': 5, 'X [m]': 3.0, 'Y [m]': 2.0, 'Apoyo': 'Libre', 'Fx [kN]': 0.0, 'Fy [kN]': -40.0},
            {'Nodo': 6, 'X [m]': 6.0, 'Y [m]': 2.0, 'Apoyo': 'Libre', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
        ])
        elements = pd.DataFrame([
            {'Barra': 1, 'Nodo i': 1, 'Nodo j': 2, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 2, 'Nodo i': 2, 'Nodo j': 3, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 3, 'Nodo i': 4, 'Nodo j': 5, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 4, 'Nodo i': 5, 'Nodo j': 6, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 5, 'Nodo i': 1, 'Nodo j': 4, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 6, 'Nodo i': 2, 'Nodo j': 5, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 7, 'Nodo i': 3, 'Nodo j': 6, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 8, 'Nodo i': 1, 'Nodo j': 5, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
            {'Barra': 9, 'Nodo i': 3, 'Nodo j': 5, 'E [GPa]': 200.0, 'A [cm2]': 20.0},
        ])
    else:
        nodes = pd.DataFrame([
            {'Nodo': 1, 'X [m]': 0.0, 'Y [m]': 0.0, 'Apoyo': 'Fijo', 'Fx [kN]': 0.0, 'Fy [kN]': 0.0},
            {'Nodo': 2, 'X [m]': 2.0, 'Y [m]': 0.0, 'Apoyo': 'Móvil X', 'Fx [kN]': 0.0, 'Fy [kN]': -10.0},
        ])
        elements = pd.DataFrame([
            {'Barra': 1, 'Nodo i': 1, 'Nodo j': 2, 'E [GPa]': 200.0, 'A [cm2]': 10.0},
        ])
    return nodes, elements


# ==============================================================================
# INTERFAZ DE USUARIO (STREAMLIT)
# ==============================================================================

st.title("🏗️ Solver de Reticulados Planos (2D)")
st.caption("Cálculo matricial de rigidez para estructuras reticuladas compuestas por barras articuladas.")

# Configuración en Sidebar
st.sidebar.header("⚙️ Configuración")
preset = st.sidebar.selectbox(
    "Cargar Estructura de Ejemplo:",
    ["Reticulado Triangular Simple", "Cercha Pratt (6 Nodos)", "Personalizado"]
)

# Carga inicial de datos
if "current_preset" not in st.session_state or st.session_state.current_preset != preset:
    st.session_state.current_preset = preset
    init_nodes, init_elements = load_example(preset)
    st.session_state.nodes = init_nodes
    st.session_state.elements = init_elements

tab1, tab2 = st.tabs(["📝 Definición de Geometría y Cargas", "📊 Resultados y Gráficos"])

with tab1:
    col_n, col_e = st.columns(2)
    
    with col_n:
        st.subheader("1. Nodos, Apoyos y Cargas")
        st.caption("Tipos de Apoyo válidos: **Fijo**, **Móvil X**, **Móvil Y**, **Libre**")
        edited_nodes = st.data_editor(
            st.session_state.nodes,
            num_rows="dynamic",
            use_container_width=True,
            key="nodes_editor"
        )
        
    with col_e:
        st.subheader("2. Barras y Propiedades de Material")
        edited_elements = st.data_editor(
            st.session_state.elements,
            num_rows="dynamic",
            use_container_width=True,
            key="elements_editor"
        )

with tab2:
    if st.button("🚀 Resolver Estructura", type="primary"):
        results, err = solve_truss(edited_nodes, edited_elements)
        
        if err:
            st.error(f"⚠️ Error en el análisis: {err}")
        else:
            st.success("¡Estructura resuelta con éxito!")
            
            # --- TABLAS DE RESULTADOS ---
            res_col1, res_col2 = st.columns(2)
            
            with res_col1:
                st.markdown("### 🔹 Desplazamientos y Reacciones")
                n_nodes = len(edited_nodes)
                U = results['U']
                R = results['R']
                
                node_res = []
                for i in range(n_nodes):
                    node_res.append({
                        'Nodo': i + 1,
                        'ux [mm]': U[2*i] * 1000.0,
                        'uy [mm]': U[2*i+1] * 1000.0,
                        'Rx [kN]': R[2*i] / 1000.0,
                        'Ry [kN]': R[2*i+1] / 1000.0
                    })
                st.dataframe(pd.DataFrame(node_res).style.format({
                    'ux [mm]': '{:.3f}', 'uy [mm]': '{:.3f}',
                    'Rx [kN]': '{:.2f}', 'Ry [kN]': '{:.2f}'
                }), use_container_width=True)

            with res_col2:
                st.markdown("### 🔹 Esfuerzos en Barras")
                forces = results['Axial_Forces']
                stresses = results['Stresses']
                
                bar_res = []
                for idx, row in edited_elements.iterrows():
                    N_val = forces[idx]
                    tipo = "Tracción" if N_val > 1e-5 else ("Compresión" if N_val < -1e-5 else "Cero")
                    bar_res.append({
                        'Barra': int(row['Barra']),
                        'Fuerza N [kN]': abs(N_val),
                        'Estado': tipo,
                        'Tensión [MPa]': stresses[idx]
                    })
                
                df_bar_res = pd.DataFrame(bar_res)
                st.dataframe(df_bar_res.style.format({
                    'Fuerza N [kN]': '{:.2f}',
                    'Tensión [MPa]': '{:.2f}'
                }), use_container_width=True)

            # --- VISUALIZACIÓN GRÁFICA ---
            st.markdown("---")
            st.markdown("### 🎨 Representación Gráfica del Reticulado")
            
            scale_factor = st.slider("Factor de escala para la deformada:", min_value=1, max_value=1000, value=100)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            # Dibujar geometría no deformada (Gris punteada)
            for _, row in edited_elements.iterrows():
                ni, nj = int(row['Nodo i']) - 1, int(row['Nodo j']) - 1
                xi, yi = edited_nodes.loc[ni, 'X [m]'], edited_nodes.loc[ni, 'Y [m]']
                xj, yj = edited_nodes.loc[nj, 'X [m]'], edited_nodes.loc[nj, 'Y [m]']
                ax.plot([xi, xj], [yi, yj], 'k--', alpha=0.3, lw=1.5, label='Original' if _ == 0 else "")

            # Dibujar geometría deformada y esfuerzos
            for idx, row in edited_elements.iterrows():
                ni, nj = int(row['Nodo i']) - 1, int(row['Nodo j']) - 1
                
                # Coordenadas originales + desplazamientos escalados
                xi = edited_nodes.loc[ni, 'X [m]'] + U[2*ni] * scale_factor
                yi = edited_nodes.loc[ni, 'Y [m]'] + U[2*ni+1] * scale_factor
                xj = edited_nodes.loc[nj, 'X [m]'] + U[2*nj] * scale_factor
                yj = edited_nodes.loc[nj, 'Y [m]'] + U[2*nj+1] * scale_factor
                
                N_val = forces[idx]
                color = 'red' if N_val < -1e-5 else ('blue' if N_val > 1e-5 else 'black')
                ax.plot([xi, xj], [yi, yj], color=color, lw=2.5)

            # Dibujar Nodos
            for idx, row in edited_nodes.iterrows():
                n = int(row['Nodo']) - 1
                xi = row['X [m]'] + U[2*n] * scale_factor
                yi = row['Y [m]'] + U[2*n+1] * scale_factor
                ax.plot(xi, yi, 'o', color='#1E3A8A', markersize=8)
                ax.text(xi, yi + 0.1, f"N{int(row['Nodo'])}", fontsize=10, fontweight='bold', ha='center')

            ax.set_aspect('equal')
            ax.set_xlabel("X [m]")
            ax.set_ylabel("Y [m]")
            ax.set_title("Estructura Deformada y Estado de Cargas (Rojo: Compresión | Azul: Tracción)")
            ax.grid(True, linestyle=':', alpha=0.6)
            
            st.pyplot(fig)
