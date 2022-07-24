from audioop import avg
from tracemalloc import start
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime
import math
import streamlit.components.v1 as components
import statsmodels.api as sm

def app():

    st.title('📊 Dashboard')

    st.markdown('### Soccer Games Data')

    st.write("The following is the DataFrame of the `games` and `appearances` datasets. You can filter your data using the sidebar selector boxes.")

    with st.sidebar:
        st.markdown('# 📧 Contact Me')

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


        dataset = st.radio('Apply the filters you want to get your data:',
            ('Player', 'Clubs'), horizontal=True)

        if dataset == "Clubs":
            type = st.radio(
            "Which club metrics do you wanna analyze?",
            ('Away', 'Home', 'General'), horizontal = True)
        else :
            type = None
        
    
    df_competitions = pd.read_csv('dataset/competitions.csv')
    df_clubs = pd.read_csv('dataset/clubs.csv')
    df_leagues = pd.read_csv('dataset/leagues.csv')
    df_games = pd.read_csv('dataset/games.csv')
    df_appearances = pd.read_csv('dataset/appearances.csv')
    df_players = pd.read_csv('dataset/players.csv')
    df_player_valuations = pd.read_csv('dataset/player_valuations.csv')


    if dataset == "Clubs":

        #Adding competition names
        df_games = pd.merge(df_games,df_competitions[['competition_id','name']],how='left', left_on = 'competition_code', right_on= 'competition_id')

        #Filtering only League competitions
        df_games = pd.merge(df_games,df_leagues[['league_id']],how='inner', left_on= 'competition_id' , right_on='league_id')

        #Adding home club names
        df_games = pd.merge(df_games,df_clubs[['club_id','pretty_name']],how='left', left_on='home_club_id', right_on ='club_id')

        #Adding away club names
        df_games = pd.merge(df_games,df_clubs[['club_id','pretty_name']],how='left', left_on='away_club_id', right_on ='club_id')

        #Changing pretty names column name
        df_games["Home_club_name"] = df_games['pretty_name_x']
        df_games["Away_club_name"] = df_games['pretty_name_y']

        #Adding result to the df
        df_games["Result"] =  np.where(df_games['home_club_goals']> df_games['away_club_goals'], 'H',
                                       np.where(df_games['home_club_goals']< df_games['away_club_goals'], 'A',  'D'))

        #Adding Home points column to df_games
        df_games['Home_points'] = np.where(df_games['Result'] =='H', 3,
                                         np.where(df_games['Result'] == 'D', 1, 0))  

        #Adding Home points column to df_games
        df_games['Away_points'] = np.where(df_games['Result'] =='H', 0,
                                         np.where(df_games['Result'] == 'D', 1, 3))  

        #Creating seasons slider selector
        years = df_games['season'].drop_duplicates().sort_values(ascending=True).astype(int).to_list()
        start_year, last_year = st.sidebar.select_slider('Select the seasons:', options=years, value = (2021,2018))

        #Creating competitions selector
        competitions = df_games['name'].drop_duplicates()
        competition_choice = st.sidebar.multiselect(
         'Select the leagues:',competitions, default = "premier-league")


        #Creating a general Dataframe appending both Away and Home dataframes
        df_away = df_games[['competition_id','name','season','round','date','Away_club_name','away_club_goals','away_club_position','Away_points']]
        df_away = df_away.rename(columns= {'Away_club_name':'Club_name','away_club_goals':'Club_goals','away_club_position':'Club_position','Away_points':'Club_points'})

        df_home = df_games[['competition_id','name','season','round','date','Home_club_name','home_club_goals','home_club_position','Home_points']]
        df_home = df_away.rename(columns= {'Home_club_name':'Club_name','home_club_goals':'Club_goals','home_club_position':'Club_position','Home_points':'Club_points'})

        df_general = pd.DataFrame
        df_general = df_general.append(df_home,df_away)

        if type == 'Away':
            away_clubs = df_games.query("name == @competition_choice").query("season >= @start_year").query("season <= @last_year")['Away_club_name'].drop_duplicates().sort_values()
            clubs_choice = st.sidebar.multiselect(
            'Select the clubs:',away_clubs)      
            df_games = df_games.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("Away_club_name == @clubs_choice")

            df_games["Goals_For"] = df_games["away_club_goals"].astype(int)
            df_games["Goals_Against"] = df_games["home_club_goals"].astype(int)

            df_away_goals = df_games.groupby(["Away_club_name","season"]).sum().reset_index().sort_values("season")

            fig_away_goals = px.line(df_away_goals, x="season",color="Away_club_name", y="Goals_For", title='Away Goals For by club', hover_data=["Goals_Against"], markers=True, text="Goals_For").update_xaxes(type='category').update_traces(textposition="top center")
            fig_away_points = px.line(df_away_goals, x="season",color="Away_club_name", y="Away_points", title='Total Away points by club', markers=True,text="Away_points").update_xaxes(type='category').update_traces(textposition="top center")      

            df_away_goals_table = df_away_goals.pivot(index='Away_club_name', columns='season', values='Goals_For')
            df_away_points_table = df_away_goals.pivot(index='Away_club_name', columns='season', values='Home_points')

            st.header("Away Metrics")
            st.plotly_chart(fig_away_goals)
            st.write(df_away_goals_table)
            st.plotly_chart(fig_away_points)
            st.write(df_away_points_table)

        elif type == 'Home':
            home_clubs = df_games.query("name == @competition_choice").query("season >= @start_year").query("season <= @last_year")['Home_club_name'].drop_duplicates().sort_values()
            clubs_choice = st.sidebar.multiselect(
            'Select the clubs:',home_clubs)      
            df_games = df_games.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("Home_club_name == @clubs_choice")

            df_games["Goals_For"] = df_games["home_club_goals"].astype(int)
            df_games["Goals_Against"] = df_games["away_club_goals"].astype(int)

            df_home_goals = df_games.groupby(["Home_club_name","season"]).sum().reset_index().sort_values("season")

            fig_home_goals = px.line(df_home_goals, x="season",color="Home_club_name", y="Goals_For", title='Home Goals For by club', hover_data=["Goals_Against"], markers=True)
            fig_home_points = px.line(df_home_goals, x="season",color="Home_club_name", y="Home_points", title='Total Home Points by club', markers=True)


            df_home_goals_table = df_home_goals.pivot(index='Home_club_name', columns='season', values='Goals_For')
            df_home_points_table = df_home_goals.pivot(index='Home_club_name', columns='season', values='Home_points')

            st.header("Home Metrics")
            st.plotly_chart(fig_home_goals)
            st.write(df_home_goals_table)
            st.plotly_chart(fig_home_points)
            st.write(df_home_points_table)


        elif type == "General":
            clubs = df_general.query("name == @competition_choice").query("season >= @start_year").query("season <= @last_year")['Club_name'].drop_duplicates().sort_values()
            clubs_choice = st.sidebar.multiselect(
            'Select the clubs you want to see',clubs)      
            df_general = df_general.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("Club_name == @clubs_choice")

            df_general['date'] = pd.to_datetime(df_general['date'])

            idx = df_general.drop_duplicates()
            idx = df_general.groupby(["season",'name','Club_name'])['date'].idxmax()

            #Creating Final position per season dataframe
            df_final_position = df_general.loc[idx]
            df_final_position = df_final_position.drop_duplicates()
            df_final_position = df_final_position[['season','Club_name','Club_position']]
            df_final_position['Club_position'] = df_final_position['Club_position'].astype(int)

            fig_club_position = px.line(df_final_position, x="season",color="Club_name", y="Club_position", title='Final club position by season', markers=True).update_xaxes(type='category').update_yaxes(autorange="reversed")

            #Total Metrics selected
            goals = df_general['Club_goals'].sum()
            points = df_general['Club_points'].sum()
            avg_position = df_final_position['Club_position'].mean()

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Goals", goals)
            col2.metric("Total Points",points)
            if math.isnan(avg_position) == True:
               col3.metric("Avg Final Position", 0)
            else: 
                col3.metric("Avg Final Position", int(avg_position))

            df_final_position = df_final_position.pivot(index='Club_name', columns='season', values='Club_position')

            st.plotly_chart(fig_club_position)
            st.write(df_final_position)


        else:
            st.write("You didn't select any data you want to analyze.")

    else:
        #Adding competition names
        df_appearances = pd.merge(df_appearances,df_competitions[['competition_id','name']],how='left', left_on = 'competition_id', right_on= 'competition_id')

        #Filtering only League competitions
        df_appearances = pd.merge(df_appearances,df_leagues[['league_id']],how='inner', left_on= 'competition_id' , right_on='league_id')

        #Adding home club names
        df_appearances = pd.merge(df_appearances,df_clubs[['club_id','pretty_name']],how='left', left_on='player_club_id', right_on ='club_id')

        #Changing pretty names column name
        df_appearances["Club_name"] = df_appearances['pretty_name']

        #Adding home club names
        df_appearances = pd.merge(df_appearances,df_players[['player_id','pretty_name','country_of_birth','position']],how='left', left_on='player_id', right_on ='player_id')

        #Changing pretty names column name
        df_appearances["Player_name"] = df_appearances['pretty_name_y']

        #Adding season to df
        df_appearances = pd.merge(df_appearances,df_games[['game_id','season']],how='left', left_on='game_id', right_on ='game_id')

        #Adding G+A column
        df_appearances['G+A'] = df_appearances['goals']+df_appearances['assists']

        #Creating seasons slider selector
        years = df_appearances['season'].drop_duplicates().sort_values(ascending=True).astype(int).to_list()
        start_year, last_year = st.sidebar.select_slider('Select the seasons:', options=years, value = (2021,2018))

        #Creating competitions selector
        competitions = df_appearances['name'].drop_duplicates()
        competition_choice = st.sidebar.multiselect(
         'Select your competitions',competitions, default = "premier-league")

        #Creating position selector
        positions = df_appearances['position'].drop_duplicates()
        position_choice = st.sidebar.multiselect(
         'Select player positions',positions, default = positions)      
        

        
        df_appearances = df_appearances.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("position == @position_choice")

        df_goals = df_appearances.groupby("Player_name").agg({'game_id':'count', 'goals': 'sum','assists':'sum','minutes_played':'sum','yellow_cards':'sum','red_cards':'sum'}).reset_index().rename(columns={'game_id':'games_played'})

        df_goals['total_minutes'] = df_goals['games_played']*90

        df_goals['goals_per_90_min'] = df_goals['goals']/df_goals['minutes_played']*90

        df_goals['assists_per_90_min'] = df_goals['assists']/df_goals['minutes_played']*90

        df_goals['G+A'] = df_goals['goals']+df_goals['assists']

        df_goals['G+A_per_90_min'] = df_goals['G+A']/df_goals['minutes_played']*90


        fig_goals = px.bar(df_goals.sort_values('goals',ascending=False).head(25), x='Player_name', y='goals', title = "Top 25 goal scorers", color='goals', hover_data= ["goals_per_90_min"],text_auto=True)
        fig_assists = px.bar(df_goals.sort_values('assists',ascending=False).head(25), x='Player_name', y='assists', title = "Top 25 assists leaders", color="assists", hover_data= ["assists_per_90_min"],text_auto=True)
        fig_g_a= px.bar(df_goals.sort_values('G+A',ascending=False).head(25), x='Player_name', y='G+A', title = "Top 25 assists leaders", color = "G+A", hover_data=["goals","assists"],text_auto=True)


        st.plotly_chart(fig_goals)
        st.write(df_goals[["Player_name","games_played","goals","goals_per_90_min","minutes_played"]].sort_values('goals',ascending=False).head(25).reset_index(drop = True))
        st.plotly_chart(fig_assists)
        st.dataframe(df_goals[["Player_name","games_played","assists","assists_per_90_min","minutes_played"]].sort_values('assists',ascending=False).head(25).reset_index(drop = True)) 
        st.plotly_chart(fig_g_a)
        st.dataframe(df_goals[["Player_name","games_played","goals","assists","G+A","G+A_per_90_min","minutes_played"]].sort_values('G+A',ascending=False).head(25).reset_index(drop = True))  

        #Joining players stats by season and player_valuations by season in single df
        df_appearances_by_season = df_appearances.groupby(["season","player_id","Player_name","country_of_birth","position"]).agg({'game_id':'count', 'goals': 'sum','assists':'sum','minutes_played':'sum','yellow_cards':'sum','red_cards':'sum'}).reset_index().rename(columns={'game_id':'games_played'})
        df_appearances_by_season['G+A'] = df_appearances_by_season['goals']+df_appearances_by_season['assists']
        df_appearances_by_season['G+A_per_90_min'] = df_appearances_by_season['G+A']/df_appearances_by_season['minutes_played']*90
        df_player_valuations['date']=pd.to_datetime(df_player_valuations['date'])
        df_player_valuations['date']=pd.DatetimeIndex(df_player_valuations['date']).year

        #Getting last valuation per season per player_id
        idx = df_player_valuations.groupby(["player_id","date"])['date'].idxmax()
        df_player_valuations = df_player_valuations.loc[idx]
     
        df_player_valuations['season'] = df_player_valuations['date']
        df_player_valuations = pd.merge(df_player_valuations,df_appearances_by_season, left_on=['season','player_id'], right_on =['season','player_id'])   

        #Filtering minimum games played
        df_player_valuations = df_player_valuations.loc[df_player_valuations['games_played'] > 12] 

        fig_g_a_vs_mkt_value = px.scatter(df_player_valuations,x='G+A', y='market_value', color='G+A_per_90_min', hover_data=['Player_name','season'],trendline="ols", title= "Player Market Value vs G+A")
        
        
        st.plotly_chart(fig_g_a_vs_mkt_value)
        st.write(df_player_valuations[['Player_name','country_of_birth','position','season','market_value','games_played','minutes_played','goals','assists','G+A','G+A_per_90_min']].sort_values('G+A', ascending= False))
        
