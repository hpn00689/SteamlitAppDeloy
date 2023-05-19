import pandas as pd
import re
import numpy as np
import streamlit as st

from scipy.stats import zscore
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Config trang -----------------------------------------
st.set_page_config(
    page_title="Model and Linear Regression",
    page_icon="🔮",
    layout="wide"
)

# Tạo tiêu đề -----------------------------------------
col1, col2, col3 = st.columns([1,5,1])

with col1:
    st.write("")
with col2:
    st.image('https://i.pinimg.com/564x/b4/10/1e/b4101eb5bc27a62b8f681bd03da9ffff.jpg')
    st.markdown("<h1 style='text-align: center; color: #B799FF;'>MODEL AND LINEAR REGRESSION</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
with col3:
    st.write("")

    

