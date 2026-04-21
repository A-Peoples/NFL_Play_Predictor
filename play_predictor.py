#importing packages
import pandas as pd
import sportsdataverse as sdv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
#modeling packages
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
st.set_page_config(page_title='NFL Penalty Charting', layout="wide")
@st.cache_data()

def load_data():
  test_dataset = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/test_dataset.csv')
  team_values = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/team_values.csv')

  return test_dataset, team_values
st.header("NFL Play Type Predictor")
test_dataset, team_values = load_data()
test_dataset = test_dataset[['posteam_num', 'defteam_num', 'down', 'ydstogo', 'posteam_pd','yardline_100', 'game_seconds_remaining', 
                             'play_type_remap', 'posteam_timeouts_remaining', 'defteam_timeouts_remaining']]

col1, col2 , col3, col4, col5 = st.columns(5)

with col1:
  home_team = st.selectbox("Home Team", team_values['posteam'].unique())
  spec_ht = team_values.loc[team_values['posteam'] == home_team]
  home_team_num = spec_ht['posteam_num'].iloc[0]
  #st.write(str(home_team_num))

  away_team = st.selectbox("Away Team", team_values['posteam'].unique())
  spec_at = team_values.loc[team_values['posteam'] == away_team]
  away_team_num = spec_at['posteam_num'].iloc[0]
  #st.write(str(away_team_num))
with col2:
  p_diff = st.number_input("Point Differential", step=1)
  yt_ez = st.slider("Yards Til Goaline", 0, 100, 75)
  
with col3:
  quarter = st.selectbox("Quarter", range(1, 5))
  minutes = st.slider("Minutes in Quarter", 0, 15, 15)
  seconds = st.slider("Seconds in Quarter", 0, 59, 0)
  if minutes == 15:
    seconds = 0
  game_sec = (3600 - (quarter * 900 - 900)) - (900 - (minutes * 60 + seconds))
  #st.write(str(game_sec))
with col4:
  down = st.selectbox("Down", range(1, 5))
  ydstogo = st.selectbox("Yards To Go", range(1, 43), 11)
  if down == 1:
    ydstogo = 10
with col5:
  h_timeouts = st.selectbox("Home Team Timeouts", range(0, 4), 3)
  a_timeouts = st.selectbox("Away Team Timeouts", range(0, 4), 3)
column_dataset = test_dataset.loc[(((test_dataset['posteam_pd'] - p_diff).isin(range(-5, 5))) & 
                                   ((test_dataset['ydstogo'] - ydstogo).isin(range(-5, 5))) & ((test_dataset['game_seconds_remaining'] - game_sec).isin(range(-60, 61)) & (test_dataset['down'] == down) & 
                                   (test_dataset['yardline_100'] - yt_ez).isin(range(-10, 10))) & 
                                   (test_dataset['posteam_timeouts_remaining'] == h_timeouts) & (test_dataset['defteam_timeouts_remaining'] == a_timeouts))].reset_index(drop=True)

st.dataframe(test_dataset, use_container_width=True)


features = ['posteam_num', 'defteam_num', 'down', 'ydstogo', 'posteam_pd','yardline_100', 'game_seconds_remaining']
labels = ['play_type_remap']

X = column_dataset[features]
y = column_dataset[labels]
def play_proba():
  if X.empty:
    st.write('No Rows Found')
    return
 
  
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  scaler = StandardScaler()
  scaler.fit(X_train)
  X_train_scaled = scaler.transform(X_train)
  
  dtc_re2 = RandomForestClassifier(max_depth=13, criterion='entropy', class_weight='balanced', n_estimators=100, random_state=42)
  dtc_re2.fit(X_train, y_train.values.ravel())
  #training
  user_checks = np.array([[home_team_num, away_team_num, down, ydstogo, p_diff, yt_ez, game_sec]])
  prob = dtc_re2.predict_proba(user_checks)[0]
  classes = dtc_re2.classes_
  
  st.write('Play Probabilities')
  st.write(str(X.shape))
  
  prob_df = pd.DataFrame({'Play_Type': classes, 'Probability': prob})   
  
  pt_map = {
 'run': 0,
 'pass': 1,
 'field_goal': 2,
 'punt': 3,
 'extra_point': 4,
 'qb_spike': 5,
 'qb_kneel': 6}
  pt_map = {v: k for k, v in pt_map.items()}
  prob_df['Play_Type'] = prob_df['Play_Type'].map(pt_map)
  st.dataframe(prob_df, use_container_width=True)
if st.button('Generate Prediction'):
  play_proba()
