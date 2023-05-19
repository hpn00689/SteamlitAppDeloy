# App streamlit to deploy the data analysis:
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

if "df" or "df_non_tech" not in st.session_state:
    st.session_state.df = None
    st.session_state.df_non_tech = None

#-------------------------------------------------------
# App title:
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")

with col2:
    st.image('https://storage.googleapis.com/kaggle-competitions/kaggle/39462/logos/header.png?t=2022-09-30-14-50-31')
    st.markdown("<h1 style='text-align: center; color: #B799FF;'>ANALYSIS OF ML/DS JOBS</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #AEE2FF;'>Vietnam and the World 2019 - 2022</h4>", unsafe_allow_html=True)

with col3:
    st.write("")    


st.markdown("---", unsafe_allow_html=True)

#-------------------------------------------------------
st.subheader("1. Thông tin về dữ liệu:")

col1, col2, col3 = st.columns([1,6,1])
with col1:
    st.write("")
with col2:
    st.image('https://media.geeksforgeeks.org/wp-content/cdn-uploads/20210301191415/Top-Kaggle-Courses-for-Data-Science.png')
with col3:
    st.write("")   


st.info("Bộ dữ liệu được lấy từ Kaggle, ở cuộc thi phân tích: (2019 - 2022) Kaggle Machine Learning & Data Science Survey (https://www.kaggle.com/competitions/kaggle-survey-2022/overview). \
        Bộ dữ liệu được Kaggle khảo sát từ người dùng để đưa ra những góc nhìn toàn diện về tình trạng của các ngành Khoa học dữ liệu và học máy. Cuộc khảo sát được thực hiện từ năm 2019 đến năm 2022. Những người khảo sát đến từ các quốc gia khác nhau, trong đó có Việt Nam.", icon="🔥")

# df = pd.read_csv('analysis_df_employee.csv')
df = pd.read_csv('app_build/analysis_df_employee.csv')
st.dataframe(df)

st.info("Ngoài bộ dữ liệu được khảo sát, nhóm còn tìm thêm một bộ dữ liệu con về các vai trò công việc trong lĩnh vực DS/ML với mức lương cơ bản của nó trong khoảng từ năm 2020 - 2021 để bổ sung phân tích cho toàn bộ bài làm của nhóm. Được lấy trên trang: https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries", icon="🔥")
# df_title_job = pd.read_csv('analysis_title_salary.csv')
df_title_job = pd.read_csv('app_build/analysis_title_salary.csv')

st.dataframe(df_title_job)

#-------------------------------------------------------
st.subheader("2. Thông tin về ứng dụng:")
st.write("""**🧑‍💻️ Tên ứng dụng**: Web app phân tích tình hình việc làm ngành Khoa học dữ liệu và học máy. \n
**👦Người thực hiện**: Nhóm 2 - Trực quan hóa dữ liệu. \n
**💻Ngôn ngữ sử dụng để trực quan**: Python. \n
**📱Framework sử dụng để triển khai**: Streamlit. \n
**📋 Chức năng của ứng dụng**: \n
- Cung cấp các biểu đồ toàn diện cũng như các thông tin về ngành.
- Cung cấp các thông số, biểu đồ thống kê mô tả.
- Cung cấp các phân tích dữ liệu đơn giản.
- Phân tích hồi quy, giải thích và dự đoán mô hình. """)

# df_non_tech = pd.read_csv("analysis_df.csv")
df_non_tech = pd.read_csv("app_build/analysis_df.csv")

st.session_state.df = df
st.session_state.df_non_tech = df_non_tech
st.session_state.df_title_job = df_title_job