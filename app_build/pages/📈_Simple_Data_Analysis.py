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
df_title_job = st.session_state.df_title_job

# if "df" or "df_non_tech" not in st.session_state:
#     df = pd.read_csv('app_build/analysis_df_employee.csv')
#     df_non_tech = pd.read_csv('app_build/analysis_df.csv')

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
st.markdown("#### 1. Kiểm định mức lương ở các công ty:")
st.info(""" **Giả thiết**: 
- H0: Mức lương chi trả ở các công ty có quy mô khác nhau thì khác nhau.
- H1: các công ty có quy mô khác nhau vẫn có mức chi trả giống nhau.
- Mức ý nghĩa: alpha = 0.05.

**Cách thực hiện**: Vì số mẫu tại các tập đều lớn hơn 30, nên ta sử dụng z-test.
""", icon="ℹ️")

code_1 = ''' 
import statsmodels.stats.weightstats as ws

Company_size_L = df[df.company_size == 'L']
Company_size_M = df[df.company_size == 'M']
Company_size_S = df[df.company_size == 'S']
Company_size_L.shape,Company_size_M.shape,Company_size_S.shape

_,pvalue_1  = ws.ztest(Company_size_L.salary_in_usd,Company_size_M.salary_in_usd,alternative='two-sided')
_,pvalue_2  = ws.ztest(Company_size_L.salary_in_usd,Company_size_S.salary_in_usd,alternative='two-sided')
_,pvalue_3  = ws.ztest(Company_size_S.salary_in_usd,Company_size_M.salary_in_usd,alternative='two-sided')
'''
st.code(code_1, language='python')

st.markdown("#### Kết quả:")
col1, col2, col3 = st.columns(3)

col1.metric(
    label="p-value (L-M)",
    value=0.0335,
)
col2.metric(
    label="p-value (L-S)",
    value=0.0129,
)
col3.metric(
    label="p-value (S-M)",
    value=0.7570,
)

st.info("""**Nhận xét**: 
- p_value < alpha tại các trường hợp công ti có quy mô lớn (L), và p_value > alpha tại trường hợp công ti nhỏ (S) và trung bình (M), khẳng định có sự khác nhau giữa công ti có quy mô lớn với các quy mô khác, trong khi không có sự khác biệt giữa công ti nhỏ và vừa.

**Kết luận:**
- Kết quả cũng không nằm ngoài dự đoán của nhiều người, khi các công ti có quy mô lớn có phúc lợi nhiều hơn các công ti khác, tuy nhiên có một điểm đáng chú ý mà cũng có thể coi là điểm tốt khi không có nhiều sự khác biệt giữa công ti nhỏ và vừa, giúp cho những người đang tìm việc có tâm lý thoải mãi hơn khi chọn lựa giữa các công ti tầm trung và nhỏ.
""", icon="📝")

st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 2. Kiểm định mức lương ở các cách thức làm việc khác nhau:")

st.info(""" **Giả thiết**:
- H0: Có sự khác biệt giữa mức lương ở các hình thức làm việc.
- H1: Hình thức làm việc không ảnh hưởng đến lương.
- Mức ý nghĩa: alpha =  0.05.

**Cách thực hiện:** Số mẫu tại các tập đều lớn hơn 30, nên tả sử dụng z-test""", icon="ℹ️")

code_2 = '''
df.remote_ratio.unique()

remote_0 = df[df.remote_ratio == 0]
remote_50 = df[df.remote_ratio == 50]
remote_100 = df[df.remote_ratio == 100]

_,pvalue_1  = ws.ztest(remote_0.salary_in_usd,remote_50.salary_in_usd,alternative='two-sided')
_,pvalue_2  = ws.ztest(remote_0.salary_in_usd,remote_100.salary_in_usd,alternative='two-sided')
_,pvalue_3  = ws.ztest(remote_50.salary_in_usd,remote_100.salary_in_usd,alternative='two-sided')
'''

st.code(code_2, language='python')

st.markdown("#### Kết quả:")
col4, col5, col6 = st.columns(3)

col4.metric(
    label="p-value (0 - 50)",
    value=0.7032,
)
col5.metric(
    label="p-value (0 - 100)",
    value=0.0611,
)
col6.metric(
    label="p-value (50 - 100)",
    value=0.0030,
)

st.info("""**Nhận xét**:
- p_value < alpha tại các trường hợp làm việc remote hoàn toàn (100%), và p_value > alpha tại trường hợp không làm việc remote (0%) và làm việc kết hợp remote (50%). Khẳng định rằng mức lương sẽ có một sự khác biệt khi ta muốn làm việc remote hoàn toàn.

**Kết luận**:
- Kết quả đưa ra không quá ngạc nhiên khi môi trường remote hoàn toàn có mức lương khác hẳn các hình thức làm việc truyền thống. 
- Tuy thế thì cũng phản ánh được một sự cần cân nhắc cho người lao động khi lựa chọn hình thức remote hoàn toàn khi đây có thể coi là 'xu hướng' làm việc của nhiều người lao động hiện tại trong ngành công nghệ.
""", icon="📝")