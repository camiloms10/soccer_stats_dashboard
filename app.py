import streamlit as st
from multiapp import MultiApp
from apps import home, data, model # import your app modules here
from streamlit_option_menu import option_menu

st.set_page_config(page_title='Camilo Manzur\'s Soccer Dashboard' ,page_icon='📊')


app = MultiApp()

# Add all your application here
app.add_app("Home", home.app)
app.add_app("Dashboard", model.app)
app.add_app("Data Extraction Tool", data.app)

# The main app
app.run()
