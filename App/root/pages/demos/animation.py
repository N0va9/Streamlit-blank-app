import streamlit as st
import numpy as np
from typing import Any
import time
 
st.title("Fractal Animation with Streamlit")
 
# --- Sidebar controls ---
mode = st.sidebar.radio("Display Mode", ["Auto", "Manual"])
iterations = st.sidebar.slider("Level of detail", 2, 20, 10, 1)
separation = st.sidebar.slider("Separation", 0.7, 2.0, 0.7885)
 
m, n, s = 960, 640, 400
x = np.linspace(-m / s, m / s, num=m).reshape((1, m))
y = np.linspace(-n / s, n / s, num=n).reshape((n, 1))
a_values = np.linspace(0.0, 4 * np.pi, 100)
 
# --- Mode Auto ---
if mode == "Auto":
    st.subheader("Automatic Animation")
    progress_bar = st.sidebar.progress(0)
    frame_text = st.sidebar.empty()
    image_placeholder = st.empty()
 
    for frame_num, a in enumerate(a_values):
        # Fractal generation
        c = separation * np.exp(1j * a)
        z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
        c_matrix = np.full((n, m), c)
        m_matrix: Any = np.full((n, m), True, dtype=bool)
        n_matrix = np.zeros((n, m))
 
        for i in range(iterations):
            z[m_matrix] = z[m_matrix] * z[m_matrix] + c_matrix[m_matrix]
            m_matrix[np.abs(z) > 2] = False
            n_matrix[m_matrix] = i
 
        # Update UI
        image_placeholder.image(1.0 - (n_matrix / n_matrix.max()), use_container_width=True)
        progress_bar.progress((frame_num + 1) / 100)
        frame_text.text(f"Frame {frame_num + 1}/100")
 
        time.sleep(0.05)  # Pause to allow display
 
    progress_bar.empty()
    frame_text.empty()
    st.button("Rerun")
 
# --- Mode Manuel ---
else:
    st.subheader("Manual Animation")
    frame = st.slider("Frame", 0, 99, 0)
    a = a_values[frame]
 
    # Fractal generation
    c = separation * np.exp(1j * a)
    z = np.tile(x, (n, 1)) + 1j * np.tile(y, (1, m))
    c_matrix = np.full((n, m), c)
    m_matrix = np.full((n, m), True, dtype=bool)
    n_matrix = np.zeros((n, m))
 
    for i in range(iterations):
        z[m_matrix] = z[m_matrix] * z[m_matrix] + c_matrix[m_matrix]
        m_matrix[np.abs(z) > 2] = False
        n_matrix[m_matrix] = i
 
    st.image(1.0 - (n_matrix / n_matrix.max()), use_container_width=True)
