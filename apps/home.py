import streamlit as st

def app():
    st.title('Home')

    st.write('This is the `home page` of this multi-page app.')

    st.markdown("""
This multi-page app is using this [Kaggle Dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores) and has a dashboard built using Pyplot and Streamlit, it also has a Data Extraction tool page.
""")
    