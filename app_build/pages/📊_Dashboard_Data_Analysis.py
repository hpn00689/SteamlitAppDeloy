import streamlit as st
import pandas as pd
import numpy as np

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# Config trang -----------------------------------------
st.set_page_config(
    page_title="Dashboard Data Analysis",
    page_icon="📊",
    layout="wide"
)

df = st.session_state.df
df_non_tech = st.session_state.df_non_tech

# Tạo tiêu đề -----------------------------------------
col1, col2, col3 = st.columns([1,6,1])

with col1:
    st.write("")
with col2:
    st.image('https://i.pinimg.com/564x/94/cd/95/94cd95a169e5aba95b51c8dad432b997.jpg')
    st.markdown("<h1 style='text-align: center; color: #B799FF;'>DASHBOARD DATA ANALYSIS</h1>", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
with col3:
    st.write("")   

# Plot thứ nhất -----------------------------------------
st.markdown("#### 1. Các nền tảng học tập nào được các kỹ sư và các học sinh tin dùng nhất?")
df_student = df_non_tech[df_non_tech['Title'] == 'Student']
df_employee = df.copy()


# Get every platfroms from everyone choice
learning_platfroms_employee = df_employee[['Learning Platforms']].apply(lambda x: 
                                                                        list( map(lambda y:y.strip(),str(x[0]).split('--'))),axis=1)\
                                                                .explode().value_counts().to_frame(name='Vote').drop(index = 'nan')
learning_platfroms = df_student[['Learning Platforms']].apply(lambda x: 
                                                      list( map(lambda y:y.strip(),str(x[0]).split('--'))),axis=1)\
                                                        .explode().value_counts().to_frame(name='Vote').drop(index = 'nan')

# --- drop un useful records
for i in learning_platfroms.index:
    if i.isnumeric():
        learning_platfroms.drop(index = i,inplace=True)
learning_platfroms.drop(index = '-1',inplace=True)

for i in learning_platfroms_employee.index:
    if i.isnumeric():
        learning_platfroms_employee.drop(index = i,inplace=True)
        
learning_platfroms_employee.drop(index = '-1',inplace=True)


# -----

learning_platfroms.reset_index(inplace=True)
learning_platfroms.rename(columns={'index':'Platfrom'},inplace=True)

learning_platfroms_employee.reset_index(inplace=True)
learning_platfroms_employee.rename(columns={'index':'Platfrom'},inplace=True)

# get top 10
learning_platfroms=learning_platfroms.sort_values('Vote',ascending=False).head(10)
learning_platfroms_employee=learning_platfroms_employee.sort_values('Vote',ascending=False).head(10)

# Plot 
fig1 = make_subplots(rows=1,cols=2,
                    specs=[[{"type": "pie"}, {"type": "pie"}]],
                    subplot_titles=("Student", "Employee"))
fig1.add_trace(go.Pie(
     name='',
     values=learning_platfroms['Vote'],
     labels=learning_platfroms['Platfrom'],hole=0.3),  
     row=1, col=1)

fig1.add_trace(go.Pie(
     name='',
     values=learning_platfroms_employee['Vote'],
     labels=learning_platfroms_employee['Platfrom'],hole=0.3),
    row=1, col=2)

fig1.update_layout(height=600, width=1600, title_text="Learning Platforms")
st.plotly_chart(fig1,use_container_width=True,height=800)


st.info("""**Nhận xét:** Với 10 nền tảng khảo sát được chọn nhiều nhất bởi 2 phía đều được giữa nguyên mà không có sự xuất hiện của một nền tảng nào khác đối với bên còn lại, dẫn đầu bởi Coursera và Udemy đã chiếm một phần phổ biến rất lớn đối với những người được khảo sát khi có đến khoảng 1/3 số người lựa chọn nền tảng này, cho thấy rằng không có sự khác biệt lớn giữa những người đi học về đã đi làm ở khoảng mục này. 
Ngoài ra, ta còn thấy việc học đại học không phải là lựa chọn ưu tiên hàng đầu cho các kỹ sư/học sinh, thay vào đó là việc học trực tuyến (có lẽ là do thời gian học tập linh hoạt nên được nhiều người lựa chọn).
""", icon="ℹ️")

st.info("""**Giải pháp thu hút người học cho những nền tảng học tập khác**: Qua việc phân tích ra nền tảng học tập nào được nhiều học sinh/kỹ sư tin dùng thì nhóm nhận thấy Coursera cũng như Udemy có nhiều lựa chọn nhất. Các giải pháp này được lựa chọn nhiều bởi vì: \n
- Có nhiều khóa học về nhiều lĩnh vực khác nhau, từ lập trình, thiết kế, kinh doanh, marketing, tài chính, v.v... Dĩ nhiên, việc học chỉ mỗi Data Science/Machine Learning thuần thôi là chưa đủ, cần phải kết hợp nhiều kiến thức từ các chuyên ngành khác vào để lấy kiến thức cho việc phân tích dữ liệu từ chúng.
- Chi phí mỗi khóa học rẻ hoặc đều miễn phí. Đối với Udemy, họ có những đợt giảm giá sâu cho những khóa học của mình, người dùng chỉ cần bỏ một khoản phí nhỏ để sở hữu được chúng. Đối với Coursera, các khóa học có hỗ trợ tài chính (miễn phí hoặc nửa giá,...) hay học dự thính (không làm bài tập, không có chứng chỉ khi học xong). Những điều này giúp cho người học tiếp cận nhiều hơn với nền tảng này.
- Các khóa học được tổ chức bài bản và khá chuyên sâu (đa số là các giảng viên đại học đến từ các trường đại học lớn trên thế giới). \n

Như vậy, để một nền tảng học tập online thu hút được nhiều người học, ta cần phải có những yếu tố như trên. Ví dụ, một nền tảng học tập mới mở thì có thể áp dụng việc giảm giá theo tuần/tháng/quý... để thu hút được nhiều người học. Ngoài ra, cung cấp nhiều kiến thức liên quan đến một bài học (bao gồm các chuyên ngành/khóa học liên quan) có thể giúp người học hiểu sâu nhất có thể. 
""", icon="❓")

#------------------------------------
# Phân tích nền tảng học tập quốc gia Việt Nam: 
# Filter Viet Nam
df_student_vi = df_student[df_student['Country'] == 'Viet Nam']
df_employee_vi = df_employee[df_employee['Country'] == 'Viet Nam']

learning_platfroms_employee_vi = df_employee_vi[['Learning Platforms']].apply(lambda x: 
                                                                        list( map(lambda y:y.strip(),str(x[0]).split('--'))),axis=1)\
                                                                .explode().value_counts().to_frame(name='Vote').drop(index = 'nan')
learning_platfroms_vi = df_student_vi[['Learning Platforms']].apply(lambda x: 
                                                      list( map(lambda y:y.strip(),str(x[0]).split('--'))),axis=1)\
                                                        .explode().value_counts().to_frame(name='Vote').drop(index = 'nan')

for i in learning_platfroms_vi.index:
    if i.isnumeric():
        learning_platfroms_vi.drop(index = i,inplace=True)
learning_platfroms_vi.drop(index = '-1',inplace=True)

for i in learning_platfroms_employee_vi.index:
    if i.isnumeric():
        learning_platfroms_employee_vi.drop(index = i,inplace=True)
        
learning_platfroms_employee_vi.drop(index = '-1',inplace=True)

learning_platfroms_vi.reset_index(inplace=True)
learning_platfroms_vi.rename(columns={'index':'Platfrom'},inplace=True)

learning_platfroms_employee_vi.reset_index(inplace=True)
learning_platfroms_employee_vi.rename(columns={'index':'Platfrom'},inplace=True)

# get top 10
learning_platfroms_vi=learning_platfroms_vi.sort_values('Vote',ascending=False).head(10)
learning_platfroms_employee_vi=learning_platfroms_employee_vi.sort_values('Vote',ascending=False).head(10)

# Plot 
fig1vi = make_subplots(rows=1,cols=2,
                    specs=[[{"type": "pie"}, {"type": "pie"}]],
                    subplot_titles=("Student", "Employee"))
fig1vi.add_trace(go.Pie(
     name='',
     values=learning_platfroms_vi['Vote'],
     labels=learning_platfroms_vi['Platfrom'],hole=0.3),  
     row=1, col=1)

fig1vi.add_trace(go.Pie(
     name='',
     values=learning_platfroms_employee_vi['Vote'],
     labels=learning_platfroms_employee_vi['Platfrom'],hole=0.3),
    row=1, col=2)

fig1vi.update_layout(height=600, width=1600, title_text="Learning Platforms In VietNam")
st.plotly_chart(fig1vi,use_container_width=True,height=800)

st.info("""**Nhận xét**: Qua 10 nền tảng học tập được khảo sát, ta thấy các kỹ sư/sinh viên Việt Nam học qua các nền tảng online như Coursera (đều chiếm 27-28%), Kaggle Learn Courses là nhiều nhất. Trong khi đó, việc học đại học lại có sự lựa chọn ít hơn nhiều. Có lẽ vì chi phí học quá cao, bỏ ra nhiều thời gian và công sức hơn so với các nền tảng online nên mới ít lựa chọn. Điều này có thể tạo ra một đội ngũ kỹ sư ít chất lượng hơn so với các nước khác (tỷ lệ học đại học cao hơn).
""", icon="ℹ️")
st.info("""**Giải pháp đề xuất cho các trường đại học thu hút nguồn sinh viên**: Việc các nền tảng học online chiếm đa số hơn với đội ngũ kỹ sư/sinh viên Việt Nam có thể là một cơ hội cho các trường đại học. Các trường có thể tạo ra các khóa học online, đặc biệt là các khóa học liên quan đến ML/DS để thu hút được nhiều sinh viên biết đến trường của mình hơn, vừa cung cấp kiến thức chuyên môn về lĩnh vực đó, vừa có thể linh hoạt giờ giấc của người học. Ngoài ra, để có thể tạo được đội ngũ kỹ sư chất lượng hơn, mang tính cạnh tranh cao hơn thì các trường nên đẩy mạnh tuyển sinh cũng như giảm học phí để người học có thể tiếp cận được kiến thức từ các trường đại học (với chi phí rẻ).
""", icon="❓")

st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 2. Các ngôn ngữ lập trình nào nào được các kỹ sư và các học sinh sử dụng cho ML/DS?")

Languages_employee = df_employee[['Languages']].apply(lambda x: 
                                                            list( map(lambda y:y.strip(),str(x[0]).split('--'))),axis=1)\
                                                    .explode().value_counts().to_frame(name='Employee')
Languages = df_student[['Languages']].apply(lambda x: 
                                            list( map(lambda y:y.strip(),str(x[0]).split('--'))),axis=1)\
                                            .explode().value_counts().to_frame(name='Student')
# --- drop un useful records
for i in Languages_employee.index:
    if i.isnumeric():
        Languages_employee.drop(index = i,inplace=True)
Languages_employee.drop(index = ['-1','nan'],inplace=True)


for i in Languages.index:
    if i.isnumeric():
        Languages.drop(index = i,inplace=True)
        
Languages.drop(index = ['-1','nan'],inplace=True)

# -----

Languages.reset_index(inplace=True)
Languages.rename(columns={'index':'Languages'},inplace=True)

Languages_employee.reset_index(inplace=True)
Languages_employee.rename(columns={'index':'Languages'},inplace=True)
Languages_use= pd.merge(Languages,Languages_employee,how='inner')

Languages_use_percent  = Languages_use
Languages_use_percent[['Student','Employee']] =  Languages_use[['Student','Employee']]/Languages_use[['Student','Employee']].sum()

# -----
plot2 = go.Figure(data=[go.Bar(
    name = 'Student',
    x = Languages_use_percent['Languages'],
    y = Languages_use_percent['Student'],
   ),
                       go.Bar(
    name = 'Employee',
    x = Languages_use_percent['Languages'],
    y = Languages_use_percent['Employee']
   )
])  
plot2.update_layout(
    xaxis_title="Languages", yaxis_title="Percentage"
)               

st.plotly_chart(plot2, use_container_width= True, height = 800)

st.info("""**Nhận xét:** Không lạ khi Python vẫn là lựa chọn hàng đầu của lĩnh vực này, và cũng không có nhiều khác biệt lớn giữa người đi làm và người chưa đi làm, ngoại trừ việc người đi làm ta thấy nhỉnh hơn về số lượng các ngôn ngữ mang chuyên tính chuyên môn 'khá hơn' như R, Bash, SQL, Scala, VBA, ... trong khi những người chưa đi làm thì có xu thế học những ngôn ngữ mang tính 'đề cử' cho người bắt đầu học như java, C hay C++.
""", icon="ℹ️")

# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 3. Việc đi làm sẽ có nhiều kinh nghiệm cho việc nghiên cứu hơn hay không?")

employee_paper = df_employee['Published Papers'].value_counts().to_frame()
not_employee_paper = df_non_tech['Published Papers'].value_counts().to_frame() - employee_paper

employee_paper.reset_index(inplace=True)
not_employee_paper.reset_index(inplace=True)

st.write(employee_paper)

fig = make_subplots(rows=1,cols=2,
                    specs=[[{"type": "pie"}, {"type": "pie"}]],
                    subplot_titles=("Employee","Unemployment"))
fig.add_trace(go.Pie(
     name='',
     values=employee_paper['count'],
     labels=employee_paper['Published Papers']),
     row=1, col=1)

fig.add_trace(go.Pie(
     name='',
     values=not_employee_paper['count'],
     labels=not_employee_paper['Published Papers']),
    row=1, col=2)

fig.update_layout(height=600, width=1000, title_text="Published Papers")
st.plotly_chart(fig, use_container_width= True, height = 800)

st.info("""**Nhận xét:** Ta có thể thấy rằng người đi làm có xu hướng có nhiều bài báo hơn so với những người chưa đi làm. Điều này có thể là do họ có nhiều kinh nghiệm hơn, hoặc có thể là do họ có nhiều thời gian hơn để nghiên cứu. 
Ngoài ra, ta có thể thấy được việc có bào báo publish hay không cũng có một phần ảnh hưởng đến khả năng có việc của những người khảo sát khi đa phần những người chưa có việc cũng chưa có bài báo publish, tuy nhiên việc này thì không mang tính bắt buộc vì khi ta xem những khảo sát thì số người có việc thì số lượng người không có bài báo publish cũng chiếm hơn 50%, tuy rằng không chiếm phần lớn như những người chưa có việc.""", icon="ℹ️")


# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 4. Số năm kinh nghiệm về việc code ảnh hưởng tới mức lương được biểu hiện như thế nào?")

# Filter out the value "I have never written code":
df_f4 = df[df['Coding Experience'] != 'I have never written code']
coding_exp_counts = df_f4['Coding Experience'].value_counts()

avg_salary = df_f4.groupby('Coding Experience')['Salary'].mean().sort_values()

fig4 = make_subplots(
    rows=1, cols=2,
    column_widths=[0.5, 0.2],
    row_heights=[2],
    subplot_titles=('Average Salary by Coding Experience', 'Coding Experience Distribution'),
    specs=[[{"type": "bar"}, {"type": "pie"}]])

fig4.add_trace(go.Bar(x=avg_salary.index, y=avg_salary.values, name='avg_salary', marker_color='red'), row=1, col=1)

fig4.add_trace(go.Pie(labels=coding_exp_counts.index, values=coding_exp_counts.values, name='coding_exp'), row=1, col=2)

fig4.update_layout(
    title='Coding Experience and Salary',
    xaxis_title="Experience",
    yaxis_title="salary",
    grid=dict(rows=1, columns=2),
    legend_title="Coding Experience",
    template='plotly_white'
)

st.plotly_chart(fig4, use_container_width= True, height = 800)

st.info("""**Nhận xét:** 
""", icon="ℹ️")

# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 5. ?")

rate_df = df.groupby(['Title', 'Gender']).size() / df.groupby('Title').size() * 100
rate_df = rate_df.reset_index(name='Rate')
rate_df = rate_df.sort_values(by='Rate')

rate_df['Gender'] = rate_df['Gender'].replace(['Nonbinary', 'Prefer to self-describe', 'Prefer not to say'], 'Others')

fig5 = go.Figure()

for gender in rate_df['Gender'].unique():
    fig5.add_trace(
        go.Bar(
            x=rate_df[rate_df['Gender'] == gender]['Title'],
            y=rate_df[rate_df['Gender'] == gender]['Rate'],
            name=gender
        )
    )

fig5.update_layout(
    title={
        'text': 'Gender Rate by Title',
        'x':0.5,
        'y': 0.95
    },
    xaxis_title='Title',
    yaxis_title='Rate (%)',
    template='plotly_white',
    barmode='group',
    legend=dict(
        orientation="h",
        yanchor="middle",
        y=1.05,
        xanchor="center",
        x=0.95
    ),
    bargap=0.2,
    autosize=False,
    width=1800,
    height=600,
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(type='category'),
    hovermode='x'
)


st.plotly_chart(fig5, use_container_width= True, height = 800)