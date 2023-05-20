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

df = pd.read_csv('app_build/analysis_df_employee.csv')
df_non_tech = pd.read_csv('app_build/analysis_df.csv')

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

fig3 = make_subplots(rows=1,cols=2,
                    specs=[[{"type": "pie"}, {"type": "pie"}]],
                    subplot_titles=("Employee","Unemployment"))
fig3.add_trace(go.Pie(
     name='',
     values=employee_paper['count'],
     labels=employee_paper['Published Papers']),
     row=1, col=1)

fig3.add_trace(go.Pie(
     name='',
     values=not_employee_paper['count'],
     labels=not_employee_paper['Published Papers']),
    row=1, col=2)

fig3.update_layout(height=600, width=1000, title_text="Published Papers")
st.plotly_chart(fig3, use_container_width= True, height = 800)

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

st.info("""**Nhận xét:** Với biểu đồ cột thứ nhất, ta có thể nhận ra được rằng kinh nghiệm code càng nhiều thì người đó có mức lương càng cao (trên 30.000 đô). Ngược lại với điều đó thì số người có kinh nghiệm code ít hơn một năm sẽ có mức lương khoảng 6.734 đô đổi lại. Biểu đồ hình tròn bổ sung thêm cho ta thấy được phần trăm người có kinh nghiệm code ít hơn một năm chiếm phần lớn (hơn 50%), vậy với ngành DS/ML nói chung, nhân lực trẻ rất là dồi dào, nhưng ngược lại thì nhân lực có kinh nghiệm rất ít. Có lẽ vì vậy mà nhìn chung, mức lương ngành này chỉ cao khi có đủ kinh nghiệm, bình thường thì không cao lắm.
""", icon="ℹ️")

# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 5. Tỷ lệ nam/nữ qua các ngành đặc thù trong lĩnh vực DS/ML được thể hiện như thế nào?")

unwanted = {'Currently not employed', 'Not employed', 'Student'}
title_list = df['Title'].value_counts().nlargest(n=14).index.to_list()
title_list = [e for e in title_list if e not in unwanted]

rate_df = df[df['Title'].isin(title_list)]
rate_df = rate_df.groupby(['Title', 'Gender']).size() / df.groupby('Title').size() * 100
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
        'text': 'Gender Rate by Occupation',
        'x':0.5,
        'y': 0.96
    },
    xaxis_title='Occupation',
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
    width=1250,
    height=600,
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(type='category'),
    hovermode='x'
)


st.plotly_chart(fig5, use_container_width= True, height = 800)

st.info("""**Nhận xét**: 
- Trong cả top 10 ngành nghề hot nhất, tỉ lệ nhân viên nam đều vượt trội hơn nhiều so với tỉ lệ nhân viên nữ (trung bình gấp ít nhất 5 lần). Điều này cho thấy ngành nghề DS/ML là một ngành nghề có tỉ lệ nam nữ mất cân đối nhất trong số các ngành nghề khác, có lẽ về vấn đề về sức khỏe (việc ngồi máy tính nhiều, ít vận động) hay vấn đề về tâm lý (việc kéo dài với cường độ cao gây stress nặng), gia đình... đã làm tỷ lệ nữ giới giảm đi đáng kể.
- Tuy nhiên, đối với công việc giáo viên/giáo sư (Teacher/Professor), tỉ lệ nam nữ khá cân đối khi tỉ lệ giáo viên nữ chỉ thua giáo viên nam khoảng hơn 10%. Vì đặc thù công việc này là truyền đạt kiến thức, nên có thể nói rằng ngành nghề này là một trong những ngành nghề có tỉ lệ nam nữ cân đối nhất.
- Manager là lĩnh vực công việc mà tỉ lệ nam vượt trội nhất so với nữ.
""", icon="ℹ️")

st.info("""**Giải pháp cho sự mất cân bằng giới tính trong ngành nghề DS/ML**:
- Đãi ngộ công việc tốt cho nữ giới, đặc biệt là những người có gia đình, ví dụ như cho phép làm việc từ xa, có chế độ nghỉ thai sản, nghỉ việc khi có con nhỏ... điều này sẽ giúp cho nữ giới có thể làm việc lâu dài hơn trong ngành nghề này.
- Tạo điều kiện cho nữ giới có thể thăng tiến trong công việc, ví dụ như tạo điều kiện cho nữ giới có thể tham gia vào các dự án lớn, có thể tham gia vào các quyết định lớn trong công ty, có thể thăng tiến lên các vị trí quản lý... điều này sẽ giúp cho nữ giới có thể có thêm động lực để tiếp tục làm việc trong ngành nghề này.
- Chế độ thăm khám sức khỏe tâm lý định kỳ cho nhân viên, đặc biệt là những nhân viên nữ giới.
""", icon="❓")

# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 6. Mối quan hệ giữa mức lương và ngành nghề:")

title_counts = df['Title'].value_counts().reset_index()
title_counts.columns = ['Title', 'Distribution']

avg_salary = df.groupby('Title')['Salary'].mean().reset_index()

color_palette = ['#FF5733', '#FFC300', '#900C3F', '#008080', '#2ECC71', '#3498DB', '#9B59B6', '#F1948A',
                 '#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF', '#C0C0C0', '#808080',
                 '#800000', '#808000', '#008000', '#800080', '#008080', '#000080', '#FFFFF0', '#F0FFF0',
                 '#F0FFFF', '#FFFAF0', '#F5F5DC', '#FAEBD7', '#FFEFD5', '#FFE4B5', '#FFE4C4']

hover_text = [
    f"{title_counts['Title'][i]}<br>Average Salary: {avg_salary['Salary'][i]:.2f}K<br>Distribution: {title_counts['Distribution'][i]}"
    for i in range(len(title_counts))
]

fig_scatter6 = go.Figure(data=go.Scatter(
    x=title_counts['Distribution'],
    y=avg_salary['Salary'],
    mode='markers',
    text=hover_text,
    hoverinfo='text',
    marker=dict(
        size=10,
        color=color_palette,
        opacity=0.8,
        line=dict(width=0.5, color='black')
    )
))

fig_scatter6.update_layout(
    title='Job Title Distribution vs Average Salary',
    xaxis_title='Distribution',
    yaxis_title='Average Salary',
    hovermode='closest',
)

st.plotly_chart(fig_scatter6, use_container_width=True)

st.info("""**Nhận xét**: 
- Data Scientist có số lượng cao nhất trong tất cả các ngành nghề, trong khi số lượng Data Journalist thì thấp nhất. Tuy nhiên, Data Scientist có mức lương có thể gọi là thấp (tầm 110000$), có lẽ vì quá nhiều nhân lực nên mức lương của ngành nghề này bị giảm xuống.
- Product/Project Manager có mức lương trung bình cao nhất, trong khi Data Architect có mức lương trung bình thấp nhất. Điều này có thể là do Data Architect là một ngành nghề mới, nên mức lương trung bình của nó còn thấp.
""", icon="ℹ️")

# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 7. Tỷ lệ phân hóa độ tuổi theo từng quốc gia qua các năm trong ngành DS/ML:")

_WIDTH = 900

# Lấy các country, get 'China', 'India', 'Viet Nam', 'United States'
df_fil_country = df[df['Country'].isin(["China🇨🇳", "India🇮🇳", "Viet Nam", "U.S.🇺🇸"])]


fig7 = px.histogram(df_fil_country,
                    x="Country", color="Age", barmode="stack", histfunc="count",
                    barnorm="percent", animation_frame="Year",
                    width=_WIDTH, height=600,
                    category_orders={"Country": ["China🇨🇳", "India🇮🇳", "Viet Nam", "U.S.🇺🇸"],
                                      "Gender":["Man", "Woman", "Prefer not to say", "Nonbinary"],
                                      "Year": range(2018,2022)},
                    title="Gender distribution of people")
fig7.update_xaxes(type='category')
fig7.update_yaxes(title="Percentage of respondents (%)")
st.plotly_chart(fig7, use_container_width=True)

st.info("""**Nhận xét**:
- Như ta có thể thấy từ biểu đồ, tỉ lệ phân hoá độ tuổi theo từng quốc gia ở Mỹ cao hơn rõ rệt so với 3 nước còn lại, số lượng người tham gia cuộc phỏng vấn là công dân Mỹ thường có thể nằm trong bất kì độ tuổi nào. Trong khi đó Việt Nam, Ấn Độ và Trung Quốc chiếm số đông là những người có độ tuổi từ 18 đến dưới 40, phần còn lại chiếm thiểu số.
- Nếu ta nhìn sâu hơn qua các năm từ 2018 đến 2022, có 1 điểm chung giữa 3 quốc gia Việt Nam, Trung Quốc và Ấn Độ là cả số lượng người thuộc độ tuổi 18-21 có cùng xu hướng tăng dần theo từng năm, đỉnh điểm là năm 2021 số lượng người tham gia cuộc phỏng vấn ở Việt Nam độ tuổi này chiếm 40%, sau đó là Ấn Độ với hơn 35% và Trung Quốc với 25%, đều cao hơn cả 3 năm trước đó. Điều này có thể lý giải được việc ngày càng có nhiều người trẻ có sự hứng thú và tham gia vào việc học cũng như làm trong mảng Machine Learning và Data Science.
- Ngoài ra, ta cũng thấy được rằng số lượng người trả lời thuộc độ tuổi 25-29 cũng chiếm phần lớn, nguyên nhân là vì đây là độ tuổi phù hợp nhất về trình độ lẫn chuyên môn trong 2 lĩnh vực Machine Learning và Data Science, tuy nhiên có 1 điểm thú vị là số lượng người ở độ tuổi này ở Mỹ thì giảm dần theo từng năm, bắt đầu với 25% số người thuộc độ tuổi này vào năm 2018 nhưng chỉ còn khoảng 14% vào năm 2022.
""", icon="ℹ️")

# -----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 8. Số năm kinh nghiệm giữa những người trong ngành DS/ML từng quốc gia qua các năm thể hiện như thế nào?")

fig8 = px.histogram(df_fil_country,
                    x="Country", color="Coding Experience", barmode="stack", histfunc="count",
                    barnorm="percent", animation_frame="Year",
                    width=_WIDTH, height=600,
                    category_orders={"Country": ["China🇨🇳", "India🇮🇳", "Viet Nam", "U.S.🇺🇸"],
                                      "Gender":["Man", "Woman", "Prefer not to say", "Nonbinary"],
                                      "Year": range(2018,2022)},
                    title="Gender distribution of people",
                )
fig8.update_xaxes(type='category')
fig8.update_yaxes(title="Percentage of respondents (%)")
st.plotly_chart(fig8, use_container_width=True)

st.info("""**Nhận xét**:
- Điểm chung giữa các biểu đồ xuyên suốt các năm từ 2018 đến 2022 là số lượng người tham gia trả lời có dưới 1 năm kinh nghiệm ở Trung Quốc, Ấn Độ và Việt Nam đều cao hơn so với cả Mỹ (trong đó cao nhất là Việt Nam vào năm 2018 với 43%)
- Số lượng người có từ 1 đến 5 năm kinh nghiệm trong lĩnh vực Data Science và Machine Learning chiếm số lượng đông đảo nhất trong cuộc phỏng vấn, tỉ lệ luôn trong khoảng 50% cho cả 4 quốc gia. Điều đó chứng tỏ rằng đây mới là nhóm người có đủ kiến thức chuyên môn và sẽ mang trọng số lớn nhất để cho ra kết quả khảo sát chính xác nhất.
- Ngoài ra, các nhóm người còn lại như những người có từ 5 đến 10 năm, 10 đến 20 năm hoặc thậm chí hơn 20 năm chiếm tỉ lệ cao nhất ở Mỹ, cao hơn hẳn so với 3 quốc gia còn lại (cụ thể nhóm người có từ 10-20 năm kinh nghiệm ở Mỹ đạt 14% năm 2020 và 16% cùng năm đó cho nhóm người có trên 20 năm kinh nghiệm), trong khi đó hầu như nhóm người đó gần như không xuất hiện ở cả 3 quốc gia kia.
""", icon="ℹ️")

#-----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 9. Mức thu nhập theo giới tính ở từng quốc gia qua các năm thể hiện như thế nào?")

avg_data = df_fil_country[df_fil_country["Gender"].isin(["Man", "Woman"])]
avg_data = avg_data[["Country", "Gender", "Salary", "Year"]]
avg_data = avg_data.dropna(subset=["Gender", "Country", "Salary", "Year"])
avg_data = avg_data.groupby(["Country", "Gender", "Year"], as_index=False).mean()


fig9 = px.bar(avg_data,
            x="Country", y="Salary",
            color="Gender",
            animation_frame="Year",
            barmode="group",
            width=_WIDTH, height=600,
            category_orders={"Country": ["China🇨🇳", "India🇮🇳", "Viet Nam", "U.S.🇺🇸"],
                            "Gender":["Man", "Woman"],
                            "Year": range(2018,2022)},
            title="Average yearly compensation of men and women",
            text="Salary")

fig9.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig9.update_layout(yaxis_range=[0,38000])
fig9.update_yaxes(title="Average yearly compensation (number of Big Macs)")
fig9.update_xaxes(type='category')

st.plotly_chart(fig9, use_container_width=True)

st.info("""**Nhận xét**:
- Về tổng quát, mức lương thường niên trung bình ở 4 quốc gia qua các năm có sự tăng giảm không hề ổn định. Tuy nhiên, đáng chú ý là trung bình thu nhập hằng năm ở Mỹ của nam luôn cao hơn nữ, lệch nhiều nhất là trong năm 2022 với hơn 35,5k đô cho nam và chỉ gần 24k cho nữ (lệch 11k đô).
- Ở 3 quốc gia còn lại, có sự thay đổi rõ rệt giữa từng năm, có những năm tổng thu nhập hằng năm của nam cao hơn, có năm thì của nữ cao hơn. Điều này cho thấy được thu nhập ở 3 quốc gia này thực sự không phải dựa trên giới tính mà nó được trả công bằng thực lực và mức độ chuyên môn của người làm trong ngành Machine Learning và Data Science.
""", icon="ℹ️")

#-----
st.markdown("---", unsafe_allow_html=True)
st.markdown("#### 10. Sự phân bổ giữa các trình độ học vấn của người tham gia khảo sát được thể hiện như thế nào?")

import plotly.figure_factory as ff

z = df.groupby(['Formal Education', 'Age']).size().unstack().fillna(0).astype('int64')
z_data = z.apply(lambda x:np.round(x/x.sum(), 2), axis = 1).to_numpy() # convert to correlation matrix
x = z.columns.tolist()
y = z.index.tolist()

fig10 = ff.create_annotated_heatmap(z_data, x = x, y = y, colorscale = "Viridis", showscale = True)

st.plotly_chart(fig10, use_container_width=True)

st.info("""**Nhận xét**:  
- Người trong khoảng độ tuổi 18 - 21 vẫn đang học và chưa có bẳng cử nhân chiếm tỉ lệ cao nhất, song song theo đó thì những người chưa qua bậc trung học vẫn chiếm một tỷ lệ vừa trong độ tuổi này.
- Từ độ tuổi 22 - 39, tỉ lệ người có bằng tiến sĩ và thạc sĩ, bằng cấp chuyên nghiệp lại chiếm cao hơn tất cả các bậc học khác, đặc biệt là ở độ tuổi 30 - 34.
- Ngoài ra, càng cao tuổi thì không có bậc học cụ thể, có thể họ ít tham gia vào bài khảo sát nên không đủ dữ liệu để phân tích.
""", icon="ℹ️")

#-----
st.markdown("---", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color:green'>DASHBOARD</h5>", unsafe_allow_html=True)

st.markdown("---", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Learning Platform Recommendation")
    st.plotly_chart(fig1, use_container_width=True, width=800)
with col2:
    st.markdown("#### Programming Languages Recommendation")
    st.plotly_chart(plot2, use_container_width=True, witdh=800)

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("#### Age & Gender & Year")
    st.plotly_chart(fig7, use_container_width=True, width=800)
with col4:
    st.markdown("#### Coding Experience & Country & Year")
    st.plotly_chart(fig8, use_container_width=True, width=800)
with col5:
    st.markdown('#### Gender & Country & Year & Salary')
    st.plotly_chart(fig9, use_container_width=True, width=800)

col6, col7 = st.columns(2)

with col6:
    st.markdown("#### Coding Experience & Salary")
    st.plotly_chart(fig4, use_container_width=True, width=800)
with col7: 
    st.markdown("#### Gender & Jobs Title")
    st.plotly_chart(fig5, use_container_width=True, width=800)

st.markdown("#### Salary & Jobs Title")
st.plotly_chart(fig_scatter6, use_container_width=True, width=800)

col8, col9 = st.columns(2)

with col8:
    st.markdown("#### Paper & Worker")
    st.plotly_chart(fig3, use_container_width=True, width=800)
with col9:
    st.markdown("#### Education & Age")
    st.plotly_chart(fig10, use_container_width=True, width=800)