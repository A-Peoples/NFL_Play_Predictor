#importing packages
import pandas as pd
import sportsdataverse as sdv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='NFL Penalty Charting', layout="wide")
@st.cache_data()

def load_data():
  test_dataset = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/test_dataset.csv')
  team_values = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/team_values.csv')

  return test_dataset, team_values

test_dataset, team_values = load_data()
col1, col2 , col3, col4 = st.columns(4)

with col1:
  home_team = st.selectbox("Home Team", team_values['posteam'].unique())
  spec_ht = team_values.loc[team_values['posteam'] == home_team]
  st.write(str(spec_ht['posteam_num'].iloc[0]))

  away_team = st.selectbox("Away Team", team_values['posteam'].unique())
  spec_at = team_values.loc[team_values['posteam'] == away_team]
  st.write(str(spec_at['posteam_num'].iloc[0]))
with col2:
  quarter = st.selectbox("Quarter", range(1, 5))
  minutes = st.slider("Minutes in Quarter", 0, 15, 15)
  seconds = st.slider("Seconds in Quarter", 0, 60, 0)
  game_sec = ((quarter * 900) - 900) + ((minutes * 60)) + (seconds)
  st.write(str(game_sec))
with col3:
  pd = st.number_input("Point Differential", step=1)
  yt_ez = st.slider("Yards Til Goaline", 0, 100, 75)
with col4:
  down = st.selectbox("Down", range(1, 5))
  ydstogo = st.selectbox("Yards To Go", range(1, 43))
st.dataframe("https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/test_dataset.csv", use_container_width=True)
