import streamlit as st
import numpy as np
import pandas as pd
import streamlit.components.v1 as components

def app():

    st.markdown("# 🔽 Data")
    
    st.markdown("### Soccer Games Data Extraction Tool")

    st.write("The following is the DataFrame of the `games` dataset. You can filter your data using the sidebar selector boxes.")

    with st.sidebar:
        st.markdown('# 📧 Contact Me ')

        with st.expander("LinkedIn"):
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

        st.markdown('# 🔎 Filters')

    df_games = pd.read_csv('dataset/games.csv')
    df_competitions = pd.read_csv('dataset/competitions.csv')
    df_clubs = pd.read_csv('dataset/clubs.csv')
    df_leagues = pd.read_csv('dataset/leagues.csv')

    #Adding competition names
    df_games = pd.merge(df_games,df_competitions[['competition_id','name']], left_on = 'competition_code', right_on= 'competition_id')

    #Filtering only League competitions
    df_games = pd.merge(df_games,df_leagues[['league_id']],how='inner', left_on= 'competition_id' , right_on='league_id')
    
    #Adding home club names
    df_games = pd.merge(df_games,df_clubs[['club_id','pretty_name']], left_on='home_club_id', right_on ='club_id')

    #Adding away club names
    df_games = pd.merge(df_games,df_clubs[['club_id','pretty_name']], left_on='away_club_id', right_on ='club_id')
    
    #Adding result to df_games
    df_games["Result"] =  np.where(df_games['home_club_goals']> df_games['away_club_goals'], 'H',
                                   np.where(df_games['home_club_goals']< df_games['away_club_goals'], 'A',  'D'))

    #Adding Home points column to df_games
    df_games['Home_points'] = np.where(df_games['Result'] =='H', 3,
                                     np.where(df_games['Result'] == 'D', 1, 0))  

    #Adding Home points column to df_games
    df_games['Away_points'] = np.where(df_games['Result'] =='H', 0,
                                     np.where(df_games['Result'] == 'D', 1, 3))  


    #Changing pretty names column name
    df_games["Home_club_name"] = df_games['pretty_name_x']
    df_games["Away_club_name"] = df_games['pretty_name_y']

    years = df_games['season'].drop_duplicates().sort_values(ascending=False)
    years_choice = st.sidebar.selectbox('Select the season:', years)
    competitions = df_games['name'].drop_duplicates()
    competition_choice = st.sidebar.multiselect(
     'Select the league:',competitions, default = "premier-league")
    clubs = df_games.query("name == @competition_choice").query("season == @years_choice")['Home_club_name'].drop_duplicates().sort_values()
    clubs_choice = st.sidebar.multiselect(
     'Select the clubs:',clubs)    
    
    df_games = df_games.query("season == @years_choice").query("name == @competition_choice").query("Home_club_name == @clubs_choice | Away_club_name == @clubs_choice")

    st.download_button(
     label="Download data as CSV 🖱️",
     data=df_games.to_csv(),
     file_name='large_df.csv',
     mime='text/csv',
 )

    st.write(df_games)