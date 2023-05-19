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

if "df" or "df_non_tech" or "df_title_job" not in st.session_state:
    df = pd.read_csv('app_build/analysis_df_employee.csv')
    df_non_tech = pd.read_csv('app_build/analysis_df.csv')
    df_title_job = pd.read_csv('app_build/analysis_title_salary.csv')

df = st.session_state.df
df_non_tech = st.session_state.df_non_tech
df_title_job = st.session_state.df_title_job

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

# Tiền xử lý dữ liệu -----------------------------------
new_df = df[["Age", "Gender", "Salary", "Title", "Formal Education", "Coding Experience", "ML Experience", "Country", "Year"]]
new_df = new_df[new_df["Country"] != "Russia🇷🇺"]
new_df = new_df[new_df["Country"] != "Australia🇦🇺"]

new_df = new_df.dropna()

# Xử lý cột tuổi:- --------------------------------------
new_df["Age"] = new_df["Age"].apply(lambda x: x.replace("+", "")).apply(lambda x: sum(map(lambda i: int(i), x.split("-"))) / len(x.split("-")))

# Xử lý cột Gender:--------------------------------------
gender_list = new_df["Gender"].unique()
gender_map = {gender: idx for gender, idx in zip(list(gender_list), range(1, len(list(gender_list)) + 1))}

new_df["Gender"] = new_df["Gender"].map(gender_map)

# Xử lý cột Title:---------------------------------------
title_list = new_df["Title"].unique()
title_map = {title: idx for title, idx in zip(list(title_list), range(1, len(list(title_list)) + 1))}
new_df["Title"] = new_df["Title"].map(title_map)

# Xử lý cột Formal Education:----------------------------
education_list = new_df["Formal Education"].unique()
education_map = {education: idx for education, idx in zip(list(education_list), [10, 7, 20, 30, 3, 15, 8])}
new_df["Formal Education"] = new_df["Formal Education"].map(education_map)

# Xử lý cột Coding Experience:---------------------------  
pattern = r'\b([0-9]+)\b'
exp_list = new_df["Coding Experience"].unique()

exp_numeric = []

for exp in exp_list:
    matches = re.findall(pattern, exp)
    numbers = [int(match[:2]) for match in matches]
    if not numbers:
        numbers = [0]
    exp_numeric.append(numbers)

exp_map = {k: sum(v) / len(v) for k, v in zip(list(exp_list), exp_numeric)}

new_df["Coding Experience"] = new_df["Coding Experience"].map(exp_map)

# Xử lý cột ML Experience:-------------------------------
ml_list = new_df["ML Experience"].unique()
ml_numeric = []

for ml in ml_list:
    matches = re.findall(pattern, ml)
    numbers = [int(match[:2]) for match in matches]
    if not numbers:
        numbers = [0]
    ml_numeric.append(numbers)

ml_map = {k: sum(v) / len(v) for k, v in zip(list(ml_list), ml_numeric)}
new_df["ML Experience"] = new_df["ML Experience"].map(ml_map)

# Xử lý cột Country:-------------------------------------
country_list = new_df["Country"].unique()
country_map = {k: v for k, v in zip(list(country_list), [5, 20, 18, 15])}
new_df["Country"] = new_df["Country"].map(country_map)

# Chia tập dữ liệu thành train và test:------------------
X = new_df.drop("Salary", axis=1)
y = new_df["Salary"]

X = X.to_numpy()
y = y.to_numpy()
y = zscore(y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----
st.markdown("<h3 style='text-align: center;'>BÀI TOÁN HỒI QUY</h3>", unsafe_allow_html=True)
st.write("Dự đoán mức lương của 1 người tham gia trả lời dựa vào 1 số thông tin cá nhân của họ.")
st.info(""" **Các cột dữ liệu được sử dụng làm feature:**
- Age: tuổi.
- Gender: giới tính.
- Title: vị trí/vai trò.
- Formal Education: bằng cấp.
- Coding Experience: số năm kinh nghiệm lập trình.
- ML Experience: số năm kinh nghiệm về machine learning.
- Country: quốc gia (gồm 4 quốc gia chính là India, China, USA, VietNam).
- Year: năm người tham gia trả lời câu hỏi.

**Cột dữ liệu được sử dụng làm target:**
- Salary: mức lương.

**Mô hình:** Linear Regression.

**Độ đo:** RMSE và MAE.
""", icon="ℹ️")

# Chọn mô hình ------------------------------------------
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

linear_predict = linear_model.predict(X_test)
linear_rmse = np.sqrt(mean_squared_error(y_test, linear_predict))
linear_mae = mean_absolute_error(y_test, linear_predict)
print("Linear Regression RMSE:", linear_rmse)
print("Linear Regression MAE", linear_mae)

# ----
col1, col2 = st.columns(2)

col1.metric(
    label="RMSE",
    value=round(linear_rmse, 3),
)
col2.metric(
    label="MAE",
    value=round(linear_mae, 3),
)

# Thử tạo mẫu dữ liệu -----------------------------------
st.markdown("<h3 style='text-align: center;'>TẠO MẪU DỮ LIỆU</h3>", unsafe_allow_html=True)

# ----
col1, col2, col3 = st.columns(3) 

age_choice = col1.slider("Tuổi", min_value=18, max_value=60, value=30, step=1) 






