import streamlit as st
import streamlit.components.v1 as components

def app():
    st.title('🏠 Home')

    st.write('This is the `home page` of this multi-page app.')

    st.markdown(""" 
This multi-page app is using this [Kaggle Dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores) and has a dashboard built using Pyplot and Streamlit, it also has a Data Extraction tool page.
""")
    with st.sidebar:

        st.markdown('# 📧 Contact Me')        

        embed_component= {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="camilo-manzur-4b7137a8" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://mx.linkedin.com/in/camilo-manzur-4b7137a8?trk=profile-badge"></a></div>""", 'medium':"""<div style="overflow-y: scroll; height:500px;"> <div id="retainable-rss-embed" 
        data-rss="https://mx.linkedin.com/in/camilo-manzur-4b7137a8?trk=profile-badge"
        data-maxcols="3" 
        data-layout="grid"
        data-poststyle="inline" 
        data-readmore="Read the rest" 
        data-buttonclass="btn btn-primary" 
        ata-offset="0"></div></div> <script src="https://www.twilik.com/assets/retainable/rss-embed/retainable-rss-embed.js"></script>"""
        }
        components.html(embed_component['linkedin'],height=250)

        st.download_button(
        label="Download Resume 🖱️",
        data='camilo_resume.pdf',
        file_name='camilo_resume.pdf',
        mime='pdf',
        )  

    with st.expander("Interactive Dashboard"):
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.image("images/dashboard_gif.gif")
            with col2:
                st.markdown("""
                    This dashboard lets you get data in multiple levels and sections like:
                      * Away, Home and General metrics by Club
                        * Goals For, Goals Against, Points
                      * Player metrics
                        * Goals, Assists, G+A, G+A per 90 min
                    """)

    with st.expander("Data extraction Tool"):
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
               st.image("images/download_gif.gif")
            with col2:
                st.markdown("""
                    This dashboard lets you extract the games.csv data filtered by:
                      * Season, league and clubs
                    """)
        
    