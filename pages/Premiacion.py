# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 01:47:07 2026

@author: Sebastian
"""

import streamlit as st

def pagina_premiacion():

    st.title("🏆 Premiación")

    st.markdown("""
    <style>
    .premiacion-title {
        text-align: center;
        font-size: 40px;
        font-weight: 800;
        color: #FFD700;
        margin-bottom: 10px;
    }

    .premiacion-sub {
        text-align: center;
        font-size: 18px;
        color: #ddd;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="premiacion-title">¡LA GLORIA TIENE SUS RECOMPENSAS!</div>', unsafe_allow_html=True)
    st.markdown('<div class="premiacion-sub">Los mejores se llevan los mejores premios</div>', unsafe_allow_html=True)

    # IMAGEN PRINCIPAL DEL PODIO
    # st.image("premiacion.png", use_container_width=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="🥇 1er Puesto", value="$700.000")

    with col2:
        st.metric(label="🥈 2do Puesto", value="$100.000")

    with col3:
        st.metric(label="🥉 3er Puesto", value="$50.000")

    st.markdown("---")

    st.success("🎉 ¡Que gane el mejor y empiece la fiesta mundialista!")