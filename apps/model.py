from tracemalloc import start
import numpy as np
import streamlit as st
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pandas as pd
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime
from apps import db

def app():

    st.title('Dashboard')

    st.markdown('### Soccer Games Data')

    st.write("The following is the DataFrame of the `games` dataset. You can filter your data using the sidebar selector boxes.")

    type = st.radio(
     "Which metrics do you wanna analyze?",
     ('Away', 'Home', 'General'))


    df_games = pd.read_csv('dataset/games.csv')
    df_competitions = pd.read_csv('dataset/competitions.csv')
    df_clubs = pd.read_csv('dataset/clubs.csv')

    #Adding competition names
    df_games = pd.merge(df_games,df_competitions[['competition_id','name']], left_on = 'competition_code', right_on= 'competition_id')
    
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
    
    
    if type == 'Away':
        away_clubs = df_games.query("name == @competition_choice").query("season >= @start_year").query("season <= @last_year")['Away_club_name'].drop_duplicates().sort_values()
        clubs_choice = st.sidebar.multiselect(
        'Select the clubs you want to see (Away Data)',away_clubs)      
        df_games = df_games.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("Away_club_name == @clubs_choice")

        df_games["Goals_For"] = df_games["away_club_goals"]
        df_games["Goals_Against"] = df_games["home_club_goals"]

        df_away_goals = df_games.groupby(["Away_club_name","season"]).sum().reset_index().sort_values("season")

        fig_away_goals = px.line(df_away_goals, x="season",color="Away_club_name", y="Goals_For", title='Away Goals For by club', hover_data=["Goals_Against"], markers=True).update_xaxes(type='category')
        fig_away_points = px.line(df_away_goals, x="season",color="Away_club_name", y="Away_points", title='Total Away points by club', markers=True).update_xaxes(type='category')       

        st.header("Away Metrics")
        st.write(df_away_goals)
        st.plotly_chart(fig_away_goals)
        st.plotly_chart(fig_away_points)
        
    elif type == 'Home':
        home_clubs = df_games.query("name == @competition_choice").query("season >= @start_year").query("season <= @last_year")['Home_club_name'].drop_duplicates().sort_values()
        clubs_choice = st.sidebar.multiselect(
        'Select the clubs you want to see (Home Data)',home_clubs)      
        df_games = df_games.query("season >= @start_year").query("season <= @last_year").query("name == @competition_choice").query("Home_club_name == @clubs_choice")

        df_games["Goals_For"] = df_games["home_club_goals"]
        df_games["Goals_Against"] = df_games["away_club_goals"]

        df_home_goals = df_games.groupby(["Home_club_name","season"]).sum().reset_index().sort_values("season")

        fig_home_goals = px.line(df_home_goals, x="season",color="Home_club_name", y="Goals_For", title='Home Goals For by club', hover_data=["Goals_Against"], markers=True).update_xaxes(type='category')
        fig_home_points = px.line(df_home_goals, x="season",color="Home_club_name", y="Home_points", title='Total Home Points by club', markers=True).update_xaxes(type='category')


        st.header("Home Metrics")
        st.plotly_chart(fig_home_goals)
        st.plotly_chart(fig_home_points)

    else:
        st.write("You didn't select any data you want to analyze.")


# Comments part

conn = db.connect()
comments = db.collect(conn)

with st.expander("💬 Open comments"):

    # Show comments

    st.write("**Comments:**")

    for index, entry in enumerate(comments.itertuples()):
        st.markdown(COMMENT_TEMPLATE_MD.format(entry.name, entry.date, entry.comment))

        is_last = index == len(comments) - 1
        is_new = "just_posted" in st.session_state and is_last
        if is_new:
            st.success("☝️ Your comment was successfully posted.")

    space(2)

    # Insert comment

    st.write("**Add your own comment:**")
    form = st.form("comment")
    name = form.text_input("Name")
    comment = form.text_area("Comment")
    submit = form.form_submit_button("Add comment")

    if submit:
        date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        db.insert(conn, [[name, comment, date]])
        if "just_posted" not in st.session_state:
            st.session_state["just_posted"] = True
        st.experimental_rerun()

