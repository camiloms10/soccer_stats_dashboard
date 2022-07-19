import streamlit as st
import streamlit.components.v1 as components

def app():
    st.title('Home')

    st.write('This is the `home page` of this multi-page app.')

    st.markdown("""
This multi-page app is using this [Kaggle Dataset](https://www.kaggle.com/datasets/davidcariboo/player-scores) and has a dashboard built using Pyplot and Streamlit, it also has a Data Extraction tool page.
""")
    with st.sidebar:

        embed_component= {'linkedin':"""<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="camilo-manzur-4b7137a8" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://mx.linkedin.com/in/camilo-manzur-4b7137a8?trk=profile-badge"></a></div>""", 'medium':"""<div style="overflow-y: scroll; height:500px;"> <div id="retainable-rss-embed" 
        data-rss="https://medium.com/feed/retainable,https://medium.com/feed/data-science-in-your-pocket"
        data-maxcols="3" 
        data-layout="grid"
        data-poststyle="inline" 
        data-readmore="Read the rest" 
        data-buttonclass="btn btn-primary" 
        ata-offset="0"></div></div> <script src="https://www.twilik.com/assets/retainable/rss-embed/retainable-rss-embed.js"></script>"""
        }
        components.html(embed_component['linkedin'],height=250)

        st.download_button(
        label="Download Resume",
        data='camilo_resume.csv',
        file_name='camilo_resume.csv',
        mime='text/csv',
        )  
    