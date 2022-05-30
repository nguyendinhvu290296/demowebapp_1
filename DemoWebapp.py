import pandas as pd
import altair as alt
import streamlit as st
import numpy as np
import pydeck as pdk
import matplotlib.pyplot as plt
import plotly.express as px
st.title("DEMO WEB_APP PHÂN TÍCH DỮ LIỆU LIÊN QUAN ĐẾN TRẬT TỰ AN TOÀN XÃ HỘI TỈNH THÁI BÌNH")
st.sidebar.selectbox(
    "Chọn dữ liệu bạn muốn thống kê",
    ('Dữ liệu trật tự xã hội', 'Dữ liệu kinh tế - ma túy - môi trường', 'Dữ liệu an toàn giao thông', 'Dữ liệu quản lý nhà nước'))
st.sidebar.button('Hiển thị')
def get_UN_data():
    df = pd.read_csv("https://raw.githubusercontent.com/nguyendinhvu290296/DemoWebapp/main/data/ttxh_app.csv") 
    return df.set_index('donvi')
def get_UN_data_2():
    df = pd.read_csv("https://raw.githubusercontent.com/nguyendinhvu290296/DemoWebapp/main/data/ttxh_app_2.csv") 
    return df.set_index('toidanh')                            
df = get_UN_data()
df2 = get_UN_data_2()
st.header("1. Biểu đồ số vụ TTXH tỉnh Thái Bình qua các năm")



st.subheader("1.1. Biểu đồ số vụ theo địa phương") 
donvi = st.multiselect("Chọn đơn vị thống kê:", list(df.index), ["TOANTINH"])
if not donvi:
    st.error("Vui lòng chọn đơn vị để hiển thị")
else:
    data_1 = df.loc[donvi]
    hover = alt.selection_single(
        fields=["Năm"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    #st.write(data.sort_index())   
    data = data_1.T.reset_index()
    data = pd.melt(data, id_vars=["index"]).rename(
        columns={"index": "Năm", "value": "Số vụ TTXH"}
    )   
    data["Năm"] = pd.to_numeric(data["Năm"])
    lines = (
        alt.Chart(data, title = "Biểu đồ số vụ liên quan đến trật tự xã hội tỉnh Thái Bình qua các năm")
        .mark_line()
        .encode(
            x="Năm:T",
            y=alt.Y("Số vụ TTXH", stack=None),
            color="donvi:N",
        )
    )
    points = lines.transform_filter(hover).mark_circle(size=65)
    tooltips = ( 
        alt.Chart(data)
        .mark_rule()
        .encode(
            x="Năm:T",
            y=alt.Y("Số vụ TTXH", stack=None),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                #alt.Tooltip("Năm", title="Năm"),
                alt.Tooltip("Số vụ TTXH", title="Số vụ"),
                alt.Tooltip("donvi", title="Đơn vị"),
            ],
        )
        .add_selection(hover)
    )
    chart = (lines+points+tooltips)
    st.altair_chart(chart, use_container_width=True)
with st.expander("Xem chi tiết số liệu"):
    st.write(df)
    




       
st.subheader("1.2. Biểu đồ số vụ theo tội danh") 
col1, col2 = st.columns(2)
df_td = pd.read_csv("https://raw.githubusercontent.com/nguyendinhvu290296/DemoWebapp/main/data/ttxh_app_2.csv")
df_td = df_td.set_index('toidanh') 
toidanh = col1.multiselect("Chọn tội danh thống kê:", list(df_td.index), ["Co y gay thuong tich"])
donvi_1 = col2.selectbox("Chọn đơn vị thống kê:", list(df.index))
if not toidanh:
    st.error("Vui lòng chọn tội danh để hiển thị")
else:
    df_td = df_td.loc[toidanh]
    hover = alt.selection_single(
        fields=["Năm"],
        nearest=True,
        on="mouseover",
        empty="none",
    )
    #st.write(data.sort_index())   
    df_td = df_td.T.reset_index()
    df_td = pd.melt(df_td, id_vars=["index"]).rename(
        columns={"index": "Năm", "value": "Số vụ"}
    )   
    df_td["Năm"] = pd.to_numeric(df_td["Năm"])
    lines = (
        alt.Chart(df_td, title = "Biểu đồ số vụ theo tội danh qua các năm")
        .mark_line()
        .encode(
            x="Năm:T",
            y=alt.Y("Số vụ", stack=None),
            color="toidanh:N",
        )
    )
    points = lines.transform_filter(hover).mark_circle(size=65)
    tooltips = ( 
        alt.Chart(df_td)
        .mark_rule()
        .encode(
            x="Năm:T",
            y=alt.Y("Số vụ", stack=None),
            opacity=alt.condition(hover, alt.value(0.3), alt.value(0)),
            tooltip=[
                #alt.Tooltip("Năm", title="Năm"),
                alt.Tooltip("Số vụ", title="Số vụ"),
                alt.Tooltip("toidanh", title="Tội danh"),
            ],
        )
        .add_selection(hover)
    )
    chart = (lines+points+tooltips)
    st.altair_chart(chart, use_container_width=True)

with st.expander("Xem chi tiết số liệu"):
    st.write(df2)





st.header("2. Biểu đồ cơ cấu tỉ lệ số vụ TTXH")

st.subheader("2.1. Cơ cấu tỷ lệ số vụ TTXH theo địa phương")

df_pie_chart = pd.read_csv("https://raw.githubusercontent.com/nguyendinhvu290296/DemoWebapp/main/data/ttxh_app.csv") 
df_pie_chart_1 = df_pie_chart.loc[df_pie_chart["donvi"] != "TOANTINH"]
data_columns = df_pie_chart_1.columns[1:]
selected_nam = st.selectbox('Chọn năm thống kê: ', data_columns)
labels = df_pie_chart_1['donvi']
sizes = df_pie_chart_1[selected_nam]
def make_autopct(sizes):
    def my_autopct(pct):
        total = sum(sizes)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%({v:d})'.format(p=pct,v=val)
    return my_autopct
explode = (0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode = explode, labels=labels, autopct=make_autopct(sizes),
        shadow=False, startangle=90, textprops=dict(color='k', fontsize=8))
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)
with st.expander("Xem chi tiết số liệu"):
    st.write(df)

st.subheader("2.2. Cơ cấu tỷ lệ số vụ TTXH theo tội danh")

df_pie_chart_td = pd.read_csv("https://raw.githubusercontent.com/nguyendinhvu290296/DemoWebapp/main/data/ttxh_app_2.csv") 
col1_td, col2_td = st.columns(2)
data_columns_td = df_pie_chart_td.columns[1:]
selected_nam_td = col1_td.selectbox('Chọn năm: ', data_columns_td)
donvi_td_1 = col2_td.selectbox("Chọn đơn vị:", list(df.index))
labels_td = df_pie_chart_td['toidanh']
sizes_td = df_pie_chart_td[selected_nam_td]
#def make_autopct_td(sizes_td):
#    def my_autopct(pct):
#        total = sum(sizes_td)
#        val = int(round(pct*total/100.0))
#        return '{p:.2f}%({v:d})'.format(p=pct,v=val)
#    return my_autopct
#fig1_td, ax1_td = plt.subplots()
#ax1_td.pie(sizes_td, explode = None, labels=labels_td, autopct=make_autopct_td(sizes_td),
#        shadow=False, startangle=90, textprops=dict(color='k', fontsize=8))
#ax1_td.axis('equal')
#st.pyplot(fig1_td)

     
        

fig = px.pie(values=sizes_td, names=labels_td, title='Biểu đồ cơ cấu tỉ lệ theo tội danh năm ' + selected_nam_td + " - " + donvi_td_1)
fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)       
with st.expander("Xem chi tiết số liệu"):
    st.write(df2)        
    
    
        
st.header("3. Dữ liệu trực quan thông qua bản đồ số tỉnh Thái Bình")

list_nam = [2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011]
st.selectbox("Chọn năm thống kê: ", list(list_nam))
df2 = pd.DataFrame(
    np.random.randn(2500, 2) / [20, 20] + [20.522948843805317, 106.42672413871823],
    columns=['lat', 'lon'])
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=20.522948843805317,
         longitude=106.42672413871823,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=df2,
            get_position='[lon, lat]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df2,
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))
def get_UN_data_3():
    df = pd.read_csv("https://raw.githubusercontent.com/nguyendinhvu290296/DemoWebapp/main/data/ttxh_app_3.csv") 
    return df.set_index('xa')                            
df3 = get_UN_data_3()
with st.expander("Xem chi tiết số liệu"):
    st.write(df3)
    
