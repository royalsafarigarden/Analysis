import pyrebase

import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

import pandas as pd
import plotly_express as px
import plotly.graph_objects as go

from PIL import Image

st.set_page_config(
    page_title="Analysis App",
    page_icon="🐘"
)

# Configuration Key
firebaseConfig = {
    'apiKey': "AIzaSyBM_B84Zjug-iF9GxP68fDERCIUoXfn-Yo",
    'authDomain': "project-c5a27.firebaseapp.com",
    'projectId': "project-c5a27",
    'storageBucket': "project-c5a27.appspot.com",
    'messagingSenderId': "120143638005",
    'appId': "1:120143638005:web:c06aa261858e1f249fc4bc",
    'measurementId': "G-9cWWD7KW79Y",
    'databaseURL': "https://project-c5a27-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

# Firebase Authentication
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Databases
db = firebase.database()
storage = firebase.storage()

logo = Image.open('images/logo.png')
st.sidebar.image(logo,
                 use_column_width=True)

# AUTHENTICATION
choice = st.sidebar.selectbox('Login / Sign Up', ['Login', 'Sign Up'])

email = st.sidebar.text_input('Please enter your email')
password = st.sidebar.text_input(
    'Please enter your password', type='password')

# SIGN UP PAGE
if choice == 'Sign Up':
    col1, col2 = st.columns([1, 2])
    col1.markdown("<h1 style='margin-top: 30px;'>Welcome to the sign up section 🎈</h1><p>After sign up you can immediately login to be able to access the app.</p>",
                  unsafe_allow_html=True)
    sign = Image.open('images/sign.png')
    col2.image(sign)

    handle = st.sidebar.text_input('Please input your name')
    submit = st.sidebar.button('Create My Account')

    if submit:
        user = auth.create_user_with_email_and_password(email, password)
        st.success('Welcome ' + handle +
                   ', your account is created successfully!')
        st.balloons()
        # Sign In
        user = auth.sign_in_with_email_and_password(email, password)
        db.child(user['localId']).child("Handle").set(handle)
        db.child(user['localId']).child("ID").set(user['localId'])
        st.info('Now you can login via login drop down selection.')

# LOGIN PAGE
if choice == 'Login':
    login = st.sidebar.checkbox('Login')
    if login:
        user = auth.sign_in_with_email_and_password(email, password)

    # NAVBAR
        selected = option_menu(
            menu_title=None,
            options=["Home", "Analysis", "Customer"],
            icons=["house", "book", "person"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "18px"},
                "nav-link": {
                    "font-family": "monospace",
                    "font-size": "18px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                },
                "nav-link-selected": {"background-color": "#c97777"},
            },
        )

        # --- HOMEPAGE ---
        if selected == "Home":
            # Banner
            banner = Image.open('images/banner.jpg')
            st.image(banner,
                     use_column_width=True)
            # Description
            st.markdown("<h2 style='text-align: center; font-family: serif;'>WELCOME</h2>",
                        unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-family: serif; font-size: 1.25rem;'>Escape from the city to the cool mountain air and lush landscape of Puncak highland. Located in Cisarua with and area of 14.000 sqm. Royal Safari Garden Resort and Convention offer a variety of recreation and educational activities at water park, rabbit garden, hydroponic, mini golf, and bird park.</p>",
                        unsafe_allow_html=True)
            st.markdown("<p style='margin-bottom: 20px; text-align: center; font-family: serif; font-size: 1.25rem;'>Preserving original design of heritage and thematic architecture and interior, the rooms at this property are warmly lit and family friendly. Royal safari garden the savanna restaurant serves Indonesian dish while sky garden restaurant serves Western food.</p>",
                        unsafe_allow_html=True)

            # Maps
            st.subheader("Our Location")
            components.iframe("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3962.743330605304!2d106.92955601431461!3d-6.678687467148565!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69b639463f5b09%3A0xd981b6c202b94ed7!2sRoyal%20Safari%20Garden%20Resort%20%26%20Convention!5e0!3m2!1sen!2sid!4v1671425535457!5m2!1sen!2sid")

            # Contact Us
            with st.container():
                st.subheader("Contact Us")
                col1, col2 = st.columns(2)
                col1.markdown(
                    "<p style='text-align: center; font-family: serif;'>Telephone : +62-251-825-3000 <br> Instagram : royalsafari_garden <br> Email : reservation@royalsafarigarden.com</p>", unsafe_allow_html=True)
                col2.markdown(
                    "<p style='text-align: center; font-family: serif;'>Fax : +62-251-825-3555 <br> Twitter : @RoyalSafari_BGR <br> Official Website : royalsafarigarden.com</p>", unsafe_allow_html=True)

        # --- ANALYSIS PAGE ---
        if selected == "Analysis":
            st.write(
                '<style>div.row-widget.stRadio > div{flex-direction:row; align-items: center;justify-content: center;}</style>', unsafe_allow_html=True)
            page = st.radio(
                'Choose :', ['Revenue', 'Market Segment', 'OTA Production'])

            placeholder = st.empty()

            if page == 'OTA Production':
                st.title('OTA Production In 2022')

                ota_data = 'data/ota.xlsx'
                df_ota = pd.read_excel(ota_data)

                groupby_col = st.selectbox(
                    'Which month you would like to analyse?',
                    ('November', 'October', 'September', 'August', 'July',
                     'June', 'May', 'April', 'March', 'February', 'January'),
                )

                # Plot Dataframe
                fig = px.bar(
                    df_ota,
                    x='OTA',
                    y=groupby_col,
                    color_discrete_sequence=['rgb(245, 186, 152)'],
                    template='ggplot2'
                )
                st.plotly_chart(fig)

                ota_chart = px.pie(df_ota,
                                   values=groupby_col,
                                   names='OTA',
                                   title=groupby_col,
                                   color_discrete_sequence=px.colors.sequential.Burgyl)
                st.plotly_chart(ota_chart)

            elif page == 'Revenue':
                # MTD Analysis
                st.title(f"Month To Date {page}")

                mtd = 'data\mtd.xlsx'
                df_mtd = pd.read_excel(mtd, sheet_name='rev')
                df_bud = pd.read_excel(mtd, sheet_name='bud')
                ps_bud = pd.pivot_table(
                    df_mtd, values=['Actual', 'Budget'], index='Month')
                ps_bud = ps_bud.reindex(['January', 'February', 'March', 'April', 'May',
                                        'June', 'July', 'August', 'September', 'October', 'November'])

                s = ps_bud.style.format({
                    'Actual': lambda x: '{:,.2f}'.format(x),
                    'Budget': lambda x: '{:,.2f}'.format(x)
                })

                groupby_col = st.selectbox(
                    'Which month you would like to analyse?',
                    ('November', 'October', 'September', 'August', 'July',
                     'June', 'May', 'April', 'March', 'February', 'January'),
                )
                col1, col2 = st.columns([2, 2.25])
                col1.dataframe(s)
                mtd_chart = px.pie(df_bud,
                                   values=groupby_col,
                                   names='Description',
                                   title=f'<b>{groupby_col} Revenue</b>',
                                   category_orders={
                                       "Description": ["Actual", "Budget"]},
                                   color_discrete_sequence=['indianred'])
                col2.plotly_chart(mtd_chart)

                # YTD Analysis
                st.title(f"Year To Date {page}")

                dataa0 = go.Scatter(
                    x=ps_bud.index,
                    y=ps_bud.Budget,
                    name='Budget',
                    text=ps_bud.Budget,
                    mode='markers + lines',
                    marker={'color': 'indianred'}
                )

                dataa1 = go.Bar(
                    x=ps_bud.index,
                    y=ps_bud.Actual,
                    name='Actual',
                    marker={'color': '#db8a8a'},
                    text=ps_bud.Actual,
                    textposition='outside',
                    texttemplate='%{text:.2f}'
                )

                data = [dataa0, dataa1]
                layout = go.Layout(title=f'<b>YTD Revenue 2022</b>',
                                   barmode='stack', template='plotly_white')
                figure = go.Figure(data=data, layout=layout)
                st.plotly_chart(figure)

                # YTD Comparison
                st.title(f"YTD {page} Comparison")

                rev_comparison = 'data/revenue_comparison.xlsx'
                df_ytd = pd.read_excel(rev_comparison,
                                       sheet_name='Revenue')

                st.dataframe(df_ytd)

                groupby_column = st.selectbox(
                    'What would you like to analyse?',
                    ('Total Revenue', 'Room Revenue',
                     'F&B Revenue', 'Other Revenue'),
                )
                # Bar Chart
                fig = px.bar(
                    df_ytd,
                    x='Year',
                    y=groupby_column,
                    color="Year",
                    color_discrete_sequence=px.colors.sequential.Redor,
                    title=f'<b>{groupby_column}</b>'
                )
                fig.update_layout(
                    title={
                        'y': 0.9,
                        'x': 0.5,
                        'xanchor': 'center',
                        'yanchor': 'top'})
                fig.update_traces(showlegend=False)
                fig.update_yaxes(title='')
                st.plotly_chart(fig)

            else:
                st.title(f"{page} {selected}")
                segment_data = 'data/market_segment.xlsx'

                # ROOM SOLD
                df_segment1 = pd.read_excel(segment_data,
                                            sheet_name='RS')

                ps = pd.pivot_table(df_segment1, values=['January', 'February', 'March', 'April', 'May',
                                    'June', 'July', 'August', 'September', 'October', 'November'], index='Segment')

                trace0 = go.Bar(
                    x=ps.index,
                    y=ps.January,
                    name='January',
                    text=ps.January,
                    marker={'color': '#FF9AA2'}
                )

                trace1 = go.Bar(
                    x=ps.index,
                    y=ps.February,
                    name='February',
                    text=ps.February,
                    marker={'color': '#FFB7B2'}
                )

                trace2 = go.Bar(
                    x=ps.index,
                    y=ps.March,
                    name='March',
                    text=ps.March,
                    marker={'color': '#FFDAC1'}
                )

                trace3 = go.Bar(
                    x=ps.index,
                    y=ps.April,
                    name='April',
                    text=ps.April,
                    marker={'color': '#ffebc1'}
                )

                trace4 = go.Bar(
                    x=ps.index,
                    y=ps.May,
                    name='May',
                    text=ps.May,
                    marker={'color': '#E2F0CB'}
                )

                trace5 = go.Bar(
                    x=ps.index,
                    y=ps.June,
                    name='June',
                    text=ps.June,
                    marker={'color': '#cbf0d2'}
                )

                trace6 = go.Bar(
                    x=ps.index,
                    y=ps.July,
                    name='July',
                    text=ps.July,
                    marker={'color': '#B5EAD7'}
                )

                trace7 = go.Bar(
                    x=ps.index,
                    y=ps.August,
                    name='August',
                    text=ps.August,
                    marker={'color': '#C7CEEA'}
                )

                trace8 = go.Bar(
                    x=ps.index,
                    y=ps.September,
                    name='September',
                    text=ps.September,
                    marker={'color': '#e3c7ea'}
                )

                trace9 = go.Bar(
                    x=ps.index,
                    y=ps.October,
                    name='October',
                    text=ps.October,
                    marker={'color': '#eab5c0'}
                )

                trace10 = go.Bar(
                    x=ps.index,
                    y=ps.November,
                    name='November',
                    text=ps.November,
                    marker={'color': '#ffc1c1'}
                )

                data = [trace0, trace1, trace2, trace3, trace4,
                        trace5, trace6, trace7, trace8, trace9, trace10]
                layout = go.Layout(title=f"<b>Room Sold</b>",
                                   template='plotly_dark')
                figure = go.Figure(data=data, layout=layout)
                figure.update_layout(title={'y': 0.9, 'x': 0.05})
                figure.update_traces(
                    texttemplate='%{text:.2f}', textposition='outside')
                figure.update_xaxes(categoryorder='array', categoryarray=[
                                    'FIT', 'OTA', 'Corp MICE', 'Gov MICE', 'Leisure'])
                st.plotly_chart(figure)

                # REVENUE
                df_segment2 = pd.read_excel(segment_data,
                                            sheet_name='Revenue')

                ps_rev = pd.pivot_table(df_segment2, values=[
                                        'FIT', 'OTA', 'Corp_MICE', 'Gov_MICE', 'Leisure'], index='Month')

                data0 = go.Bar(
                    x=ps_rev.index,
                    y=ps_rev.FIT,
                    name='FIT',
                    text=ps_rev.FIT,
                    marker={'color': 'rgb(242, 167, 162)'}
                )

                data1 = go.Bar(
                    x=ps_rev.index,
                    y=ps_rev.OTA,
                    name='OTA',
                    text=ps_rev.OTA,
                    marker={'color': 'rgb(252, 215, 189)'}
                )

                data2 = go.Bar(
                    x=ps_rev.index,
                    y=ps_rev.Corp_MICE,
                    name='Corp MICE',
                    text=ps_rev.Corp_MICE,
                    marker={'color': 'rgb(226, 240, 203)'}
                )

                data3 = go.Bar(
                    x=ps_rev.index,
                    y=ps_rev.Gov_MICE,
                    name='Gov MICE',
                    text=ps_rev.Gov_MICE,
                    marker={'color': 'rgb(181, 234, 215)'}
                )

                data4 = go.Bar(
                    x=ps_rev.index,
                    y=ps_rev.Leisure,
                    name='Leisure',
                    text=ps_rev.Leisure,
                    marker={'color': 'rgb(199, 206, 234)'}
                )

                data = [data0, data1, data2, data3, data4]
                layout = go.Layout(title=f"<b>Room Revenue</b>",
                                   barmode='stack', template='plotly_dark')
                figure = go.Figure(data=data, layout=layout)
                figure.update_traces(text=None)
                figure.update_layout(title={'y': 0.9, 'x': 0.05})
                figure.update_xaxes(categoryorder='array', categoryarray=[
                                    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November'])
                st.plotly_chart(figure)

        # --- CUSTOMER PAGE ---
        if selected == "Customer":
            st.title(f"{selected} Analysis In 2022")

            customer = 'data/customer.xlsx'
            df1 = pd.read_excel(customer,
                                sheet_name='2021')
            df2 = pd.read_excel(customer,
                                sheet_name='2022')

            # MAPS
            # st.header('City & Country')
            col1, col2 = st.columns([1, 6])
            col1.markdown(
                "<h3 style='margin-left: 5px;'>Top 5 City :</h3>", unsafe_allow_html=True)
            col1.markdown(
                "<h6 style='margin-left: 5px;'>1. Jakarta<br>2. Tangerang<br>3. Bekasi<br>4. Bogor<br>5. Depok</h6>", unsafe_allow_html=True)
            fig = px.scatter_geo(df2,
                                 lat='Lat',
                                 lon='Lon',
                                 color='Country',
                                 hover_name='City')
            col2.write(fig)

            # GENDER COMPARISON
            st.markdown(
                "<h1 style='text-align: center;'>Gender Distribution Comparison</h1>", unsafe_allow_html=True)

            tab1, tab2 = st.tabs(["2022", "2021"])

            tab1.subheader("Gender Distribution by 2022")
            gen2022 = df2['Gender'].value_counts()
            gen_name22 = ['Female', 'Male']

            fig = px.pie(
                df2,
                values=gen2022,
                names=gen_name22,
                color_discrete_sequence=px.colors.sequential.dense)
            tab1.write(fig)

            tab2.subheader("Gender Distribution by 2021")
            gen2021 = df1['Gender'].value_counts()
            gen_name21 = ['Male', 'Female']

            fig = px.pie(
                df2,
                values=gen2021,
                names=gen_name21,
                color_discrete_sequence=px.colors.sequential.Purp)
            tab2.write(fig)

    else:
        st.markdown("<h1 style='text-align: center;'>Welcome, you must login first<br>in order to access the app</h1>",
                    unsafe_allow_html=True)
        banner_welc = Image.open('images/stat.png')
        st.image(banner_welc,
                 use_column_width=True)
        st.markdown("<h6 style='text-align: center; font-family: monospace;'>If you don't have any account, you can sign up first.</h6>",
                    unsafe_allow_html=True)

# COPYRIGHT
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer:before{
                    content:'© 2022 Claudia Hanna Aurelly Mamahit';
                    display: flex;
                    justify-content: center;
                    color:gray;
                }
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
