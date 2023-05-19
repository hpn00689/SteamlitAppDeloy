import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Config trang -----------------------------------------
st.set_page_config(
    page_title="Data Analysis",
    page_icon="🧮",
    layout="wide"
)

df = st.session_state.df
df_non_tech = st.session_state.df_non_tech
df_title_job = st.session_state.df_title_job

if "df" or "df_non_tech" or "df_title_job" not in st.session_state:
    df = pd.read_csv('app_build/analysis_df_employee.csv')
    df_non_tech = pd.read_csv('app_build/analysis_df.csv')
    df_title_job = pd.read_csv('app_build/analysis_title_salary.csv')
    
# Tạo tiêu đề -----------------------------------------
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")
with col2:
    st.image('https://i.pinimg.com/564x/42/15/82/4215828147e9d7f55b41c77e0240b925.jpg')
    st.markdown("<h1 style='text-align: center; color: #B799FF;'>DASHBOARD STATISCAL DESCRIPTION</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
with col3:
    st.write("")    

# Giá trị - Các biến quan sát -------------------------
st.markdown("#### 1. Thông tin về dữ liệu:")
st.markdown("##### 1.1 Dữ liệu khảo sát:")
# Chưa lọc tech workers:
st.markdown("<h5 style='text-align: center; color:green'>Đối với dữ liệu chưa được lọc tech workers:</h5>", unsafe_allow_html=True)

# Tạo các cột:
data_inf1, data_inf2, data_inf3, data_inf4 = st.columns(4)

data_inf1.metric(
    label="Số lượng quan sát",
    value=df_non_tech.shape[0],
)
data_inf2.metric(
    label="Số lượng thuộc tính",
    value=df_non_tech.shape[1],
)
data_inf3.metric(
    label="SỐ lượng thuộc tính số",
    value=df_non_tech.select_dtypes(include=np.number).shape[1],
)
data_inf4.metric(
    label="Số lượng thuộc tính phân loại",
    value=df_non_tech.shape[1] - df_non_tech.select_dtypes(include=np.number).shape[1],
)

# Lọc tech workers:
st.markdown("<h5 style='text-align: center; color:green'>Đối với dữ liệu lọc tech workers:</h5>", unsafe_allow_html=True)

# Tạo các cột:
data_inf5, data_inf6, data_inf7, data_inf8 = st.columns(4)

data_inf5.metric(
    label="Số lượng quan sát",
    value=df.shape[0],
)
data_inf6.metric(
    label="Số lượng thuộc tính",
    value=df.shape[1],
)
data_inf7.metric(
    label="SỐ lượng thuộc tính số",
    value=df.select_dtypes(include=np.number).shape[1],
)
data_inf8.metric(
    label="Số lượng thuộc tính phân loại",
    value=df.shape[1] - df.select_dtypes(include=np.number).shape[1],
)

st.markdown("##### 1.2 Dữ liệu lương theo vai trò:")
data_inf9, data_inf10, data_inf11, data_inf12 = st.columns(4)

data_inf9.metric(
    label="Số lượng quan sát",
    value=df_title_job.shape[0],
)
data_inf10.metric(
    label="Số lượng thuộc tính",
    value=df_title_job.shape[1],
)
data_inf11.metric(
    label="SỐ lượng thuộc tính số",
    value=df_title_job.select_dtypes(include=np.number).shape[1],
)
data_inf12.metric(
    label="Số lượng thuộc tính phân loại",
    value=df_title_job.shape[1] - df_title_job.select_dtypes(include=np.number).shape[1],
)


st.markdown("---", unsafe_allow_html=True)

# Lọc DataFrame theo năm -------------------------------
st.markdown("##### Bộ lọc năm toàn cục:", unsafe_allow_html=True)

year_filter = st.selectbox("Lọc theo năm:", df['Year'].unique())
df_year = df[df["Year"] == year_filter]

# Tính năm trước với năm đã được chọn:
if year_filter == 2018:
    pre_year = 2018
else:
    pre_year = year_filter - 1

df_pre_year = df[df["Year"] == pre_year]

# Lấy các độ đo thống kê:
df_describe = df_year.describe().round(2).T
df_describe_pre = df_pre_year.describe().round(2).T

# Dashboard về lương của thế giới ---------------------
st.markdown("#### 2. Thông số thống kê về Salary ($):")
st.markdown("<h4 style='text-align: center; color:green'>Tổng hợp từ 6 quốc gia</h4>", unsafe_allow_html=True)

# Tạo các cột để hiển thị thông số thống kê (P1):
stats_age_col1, stats_age_col2, stats_age_col3, stats_age_col4 = st.columns(4)
stats_age_col1.metric(
    label="Mean",
    value=df_describe.loc["Salary"].loc["mean"],
    delta=round(df_describe.loc["Salary"].loc["mean"] - df_describe_pre.loc["Salary"].loc["mean"], 2),
)
stats_age_col2.metric(
    label="Median",
    value=df_describe.loc["Salary"].loc["50%"],
    delta=round(df_describe.loc["Salary"].loc["50%"] - df_describe_pre.loc["Salary"].loc["50%"], 2),
)
stats_age_col3.metric(
    label="Std",
    value=df_describe.loc["Salary"].loc["std"],
    delta=round(df_describe.loc["Salary"].loc["std"] - df_describe_pre.loc["Salary"].loc["std"], 2),
)
stats_age_col4.metric(
    label="Count",
    value=df_describe.loc["Salary"].loc["count"].astype(int),
    delta=round(df_describe.loc["Salary"].loc["count"] - df_describe_pre.loc["Salary"].loc["count"], 2),
)

# Tạo các cột để hiển thị thông số thống kê (P2):
stats_age_col5, stats_age_col6, stats_age_col7 = st.columns(3)
stats_age_col5.metric(
    label="25%",
    value=df_describe.loc["Salary"].loc["25%"],
    delta=round(df_describe.loc["Salary"].loc["25%"] - df_describe_pre.loc["Salary"].loc["25%"], 2),
)
stats_age_col6.metric(
    label="Min",
    value=df_describe.loc["Salary"].loc["min"],
    delta=round(df_describe.loc["Salary"].loc["min"] - df_describe_pre.loc["Salary"].loc["min"], 2),
)
stats_age_col7.metric(
    label="Max",
    value=df_describe.loc["Salary"].loc["max"],
    delta=round(df_describe.loc["Salary"].loc["max"] - df_describe_pre.loc["Salary"].loc["max"], 2),
)

# Tạo box plox cho Salary thế giới:
fig_boxplot_world = px.box(df_year, y="Salary")
st.plotly_chart(fig_boxplot_world,use_container_width=True,height=800)

# Dashboard về lương của từng quốc gia -----------------
st.markdown("<h4 style='text-align: center; color:green'>Chọn quốc gia cụ thể</h4>", unsafe_allow_html=True)

# Lọc dataframe theo quốc gia:
country_filter = st.selectbox("Lọc theo quốc gia:", df['Country'].unique())

df_country = df_year[df_year["Country"] == country_filter]
df_describe_country = df_country.describe().T
df_pre_describe_country = df_pre_year[df_pre_year["Country"] == country_filter].describe().T

# Tạo các cột để hiển thị thông số thống kê (P1):
country_col1, country_col2, country_col3, country_col4 = st.columns(4)
country_col1.metric(
    label="Mean",
    value=round(df_country["Salary"].mean(), 2),
    delta=round(df_describe_country.loc["Salary"].loc["mean"] - df_pre_describe_country.loc["Salary"].loc["mean"], 2),
)
country_col2.metric(
    label="Median",
    value=round(df_country["Salary"].median(), 2),
    delta=round(df_describe_country.loc["Salary"].loc["50%"] - df_pre_describe_country.loc["Salary"].loc["50%"], 2),
)
country_col3.metric(
    label="Std",
    value=round(df_country["Salary"].std(), 2),
    delta=round(df_describe_country.loc["Salary"].loc["std"] - df_pre_describe_country.loc["Salary"].loc["std"], 2),
)
country_col4.metric(
    label="Count",
    value=df_country["Salary"].count().astype(int),
    delta=round(df_describe_country.loc["Salary"].loc["count"] - df_pre_describe_country.loc["Salary"].loc["count"], 2),
)

# Tạo các cột để hiển thị thông số thống kê (P2):
country_col5, country_col6, country_col7 = st.columns(3)
country_col5.metric(
    label="25%",
    value=df_country["Salary"].quantile(0.25),
    delta=round(df_describe_country.loc["Salary"].loc["25%"] - df_pre_describe_country.loc["Salary"].loc["25%"], 2),
)
country_col6.metric(
    label="Min",
    value=df_country["Salary"].min(),
    delta=round(df_describe_country.loc["Salary"].loc["min"] - df_pre_describe_country.loc["Salary"].loc["min"], 2),
)
country_col7.metric(
    label="Max",
    value=df_country["Salary"].max(),
    delta=round(df_describe_country.loc["Salary"].loc["max"] - df_pre_describe_country.loc["Salary"].loc["max"], 2),
)

# Tạo box plox cho Salary theo quốc gia:
fig_boxplot_country = px.box(df_country, y="Salary", x="Country")
st.plotly_chart(fig_boxplot_country,use_container_width=True,height=800)

st.markdown("---", unsafe_allow_html=True)

# Dashboard về biểu đồ thống kê -----------------
st.markdown("#### 3. Các biểu đồ mô tả:")

# Lấy số lượng người phân phối theo tuổi:
df_age = df.groupby(['Age', 'Year']).size().reset_index(name='Count')
df_age = df_age[df_age["Year"] == year_filter]

# Tạo dashboard, cột về biểu đồ thống kê (P1):
fig_col1, fig_col2 = st.columns([5, 5])
with fig_col1:
    st.markdown("### Tech workers")
    fig_tech_worker = px.histogram(df,
                    x="Year", color="Country", barmode="group", histfunc="count",
                    category_orders={"Country": ["China🇨🇳", "India🇮🇳", "Viet Nam", "U.S.🇺🇸"]})
    fig_tech_worker.update_xaxes(type='category')
    fig_tech_worker.update_yaxes(title="Number of tech workers")

    st.plotly_chart(fig_tech_worker,use_container_width=True,height=800)
with fig_col2:
    st.markdown("### Age range percentage")
    fig_age_range = px.pie(df_age, values='Count', names='Age')
    st.plotly_chart(fig_age_range,use_container_width=True,height=800)


# Tạo dashboard, cột về biểu đồ thống kê (P2):
fig_col3, fig_col4 = st.columns([5, 5])
with fig_col3:
    st.markdown("### Salary histogram")
    fig_salary_hist = px.histogram(df_year, x="Age", y='Salary', hover_data=df.columns)
    st.plotly_chart(fig_salary_hist,use_container_width=True,height=800)
with fig_col4:
    st.markdown("### Salary boxplot")
    fig_salary_boxplot = px.box(df_year, x="Age", y='Salary', hover_data=df.columns)
    st.plotly_chart(fig_salary_boxplot,use_container_width=True,height=800)

# Tiến hành nhận xét -----------------
st.markdown("#### 4. Các nhận xét hữu ích từ biểu đồ/thông số thống kê:")

st.markdown("##### 4.1 Bộ dữ liệu chính:")
tab1, tab2, tab3, tab4 = st.tabs(["Box Plot", "Tech Workers", "Age Range", "Salary Histogram"])
with tab1:
    st.markdown("##### 1. Box Plot:")

    col_tab1_1, col_tab1_2 = st.columns([4, 6])
    year_filter_tab = col_tab1_1.selectbox("Chọn năm thể hiện box plot", df['Year'].unique())
    df_year_tab = df[df["Year"] == year_filter_tab]

    df_describe_tab = df_year_tab.describe().round(2).T
    fig_boxplot_world_tab = px.box(df_year_tab, y="Salary")

    with col_tab1_1:
        st.caption(f"1.1. Phân bổ lương DS/ML năm {year_filter_tab}")
        st.plotly_chart(fig_boxplot_world_tab,use_container_width=True,height=800)
    with col_tab1_2:
        year_filter_tab5 = col_tab1_2.selectbox("Chọn năm khảo sát phân bổ lương theo tuổi", df['Year'].unique())
        st.caption(f"5.1. Phân bổ lương theo độ tuổi của tech workers trong năm {year_filter_tab5} ")

        df_year_tab5 = df[df["Year"] == year_filter_tab5]
        df_salary_tab5 = px.box(df_year_tab5, x="Age", y='Salary', hover_data=df.columns)

        st.plotly_chart(df_salary_tab5,use_container_width=True,height=800)

with tab2:
    st.markdown("##### 2. Tech Workers:")

    col_tab2_1, col_tab2_2 = st.columns([4, 6])

    with col_tab2_1:
        st.caption(f"2.1. Số lượng tech workers (tham gia khảo sát) theo từng quốc gia")
        st.plotly_chart(fig_tech_worker,use_container_width=True,height=800)
    with col_tab2_2:
        st.info("**Nhận xét chung**: Qua thời gian từ 2019 đến 2022, có thể nhận thấy Việt Nam và sau đó là Trung Quốc là hai quốc gia có số lượng người tham gia khảo sát ít nhất. Đáng chú ý, sự tham gia của người dân trong mỗi quốc gia không phản ánh tỷ lệ dân số của quốc gia đó. Chẳng hạn, vào năm 2021, dân số Trung Quốc là khoảng 1,412 tỷ, dân số Ấn Độ là 1,393 tỷ, dân số Việt Nam là 97,5 triệu và dân số Hoa Kỳ là khoảng 331,9 triệu. Điều này có nghĩa là trong cuộc khảo sát năm 2021, các nhân viên công nghệ chiếm tỷ lệ (5,76e-7)% trong dân số Trung Quốc, (6,31e-6)% trong dân số Ấn Độ, (2.1e-6)% trong dân số Việt Nam và (8,79e-6)% trong dân số Mỹ.")

with tab3:
    st.markdown("##### 3. Age Range:")
    col_tab3_1, col_tab3_2 = st.columns([4, 6])
    

    with col_tab3_1:
        year_filter_tab3 = col_tab3_1.selectbox("Chọn năm khảo sát tuổi", df['Year'].unique())
        st.caption(f"3.1. Phân bổ theo độ tuổi của tech workers trong năm {year_filter_tab3}")
        
        df_age_t3 = df.groupby(['Age', 'Year']).size().reset_index(name='Count')
        df_age_tab3 = df_age_t3[df_age_t3["Year"] == year_filter_tab3]
        df_age_tab3 = px.pie(df_age_tab3, values='Count', names='Age')

        st.plotly_chart(df_age_tab3,use_container_width=True,height=800)
    with col_tab3_2:
        st.info(f"**Nhận xét chung**: Độ tuổi của tech workers tham gia khảo sát tập trung chủ yếu trong khoảng từ 25 đến 34 tuổi. Từ đó giảm dần về các độ tuổi còn lại. Điều này có thể giải thích bởi độ tuổi này là độ tuổi mà người ta đã tốt nghiệp đại học và bắt đầu đi làm. Đồng thời, độ tuổi này cũng là độ tuổi mà người ta có thể có gia đình và có con. Vì vậy, họ sẽ có nhu cầu tìm kiếm một công việc ổn định và lương cao dựa trên kinh nghiệm của mình hơn để có thể nuôi sống cho gia đình của mình")

with tab4:
    st.markdown("##### 4. Salary Histogram:")
    col_tab4_1, col_tab4_2 = st.columns([4, 6])

    with col_tab4_1:
        year_filter_tab4 = col_tab4_1.selectbox("Chọn năm khảo sát lương", df['Year'].unique())
        st.caption(f"4.1. Phân bổ lương theo độ tuổi của tech workers trong năm {year_filter_tab4} ")

        df_year_tab4 = df[df["Year"] == year_filter_tab4]
        df_salary_tab4 = px.histogram(df_year_tab4, x="Age", y='Salary', hover_data=df.columns)

        st.plotly_chart(df_salary_tab4,use_container_width=True,height=800)
    with col_tab4_2:
        st.info(f"**Nhận xét chung**: Qua từng năm, ta có thể thấy rằng lương của tech workers tăng dần theo độ tuổi, cụ thể là từ hơn 30 đến 50 tuổi rồi bắt đầu hạ xuống dần, điều này có thể được phỏng đoán dựa vào độ tuổi càng cao thì số kinh nghiệm họ tích góp được càng nhiều và lên chức vụ nếu đã làm lâu năm, nhưng sau độ tuổi 50 thì họ bắt đầu về hưu cho nên lương giảm mạnh. Ở độ tuổi 22 - 29, lương vẫn còn chưa cao vì có thể họ mới tìm được việc làm hay trong kỳ thực tập... ")

st.markdown("##### 4.2 Bộ dữ liệu phụ:")

tab5, tab6 = st.tabs(["Thông số Salary (USD)", "Tỷ lệ làm remote (%)"])

with tab5:
    col_tab5_1, col_tab5_2 = st.columns(2)

    with col_tab5_1:
        df_salary_title_tab = df_title_job["salary_in_usd"].describe().T
        st.dataframe(df_salary_title_tab)
    with col_tab5_2:
        fig_salary_title_tab = px.box(df_title_job, y="salary_in_usd")
        st.plotly_chart(fig_salary_title_tab,use_container_width=True, width=900)
with tab6:
    col_tab6_1, col_tab6_2 = st.columns(2)

    with col_tab6_1:
        df_remote_title_tab = df_title_job["remote_ratio"].describe().T
        st.dataframe(df_remote_title_tab)

    with col_tab6_2:
        fig_remote_title_tab = px.box(df_title_job, y="remote_ratio")
        st.plotly_chart(fig_remote_title_tab,use_container_width=True, width=900)