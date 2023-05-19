import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Config trang -----------------------------------------
st.set_page_config(
    page_title="Simple Data Analysis",
    page_icon="📈",
    layout="wide"
)

df = st.session_state.df
df_non_tech = st.session_state.df_non_tech

# Tạo tiêu đề -----------------------------------------
col1, col2, col3 = st.columns([1,5,1])

with col1:
    st.write("")
with col2:
    st.image('https://i.pinimg.com/564x/f8/04/2a/f8042ae4a7f5c348ec961dbb6a660174.jpg')
    st.markdown("<h1 style='text-align: center; color: #B799FF;'>SIMPLE DATA ANALYSIS</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
with col3:
    st.write("")    

# Giá trị - Các biến quan sát -------------------------
st.markdown("#### 1. Thông tin về dữ liệu:")


