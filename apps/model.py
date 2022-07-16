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

def app():

    st.title('Dashboard')

    st.markdown('### Soccer Games Data')

    st.write("The following is the DataFrame of the `games` dataset. You can filter your data using the sidebar selector boxes.")

    with st.sidebar:
            type = st.radio(
     "Which metrics do you wanna analyze?",
     ('Away', 'Home', 'General'))


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
     'Select your competitions',competitions, default = "premier-league")

    
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
        'Select the clubs you want to see (Away Data)',away_clubs)      
        df_games = df_games.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("Away_club_name == @clubs_choice")

        df_games["Goals_For"] = df_games["away_club_goals"].astype(int)
        df_games["Goals_Against"] = df_games["home_club_goals"].astype(int)

        df_away_goals = df_games.groupby(["Away_club_name","season"]).sum().reset_index().sort_values("season")

        fig_away_goals = px.line(df_away_goals, x="season",color="Away_club_name", y="Goals_For", title='Away Goals For by club', hover_data=["Goals_Against"], markers=True).update_xaxes(type='category')
        fig_away_points = px.line(df_away_goals, x="season",color="Away_club_name", y="Away_points", title='Total Away points by club', markers=True).update_xaxes(type='category')       

        st.header("Away Metrics")
        st.plotly_chart(fig_away_goals)
        st.plotly_chart(fig_away_points)
        
    elif type == 'Home':
        home_clubs = df_games.query("name == @competition_choice").query("season >= @start_year").query("season <= @last_year")['Home_club_name'].drop_duplicates().sort_values()
        clubs_choice = st.sidebar.multiselect(
        'Select the clubs you want to see (Home Data)',home_clubs)      
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

