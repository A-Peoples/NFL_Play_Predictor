#importing packages
import pandas as pd
import sportsdataverse as sdv
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title='NFL Penalty Charting', layout="wide")
#@st.cache_data()

def load_data():
  X_train = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/X_train.csv')
  X_test = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/X_test.csv')
  y_train = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/y_train.csv')
  y_test = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/y_test.csv')
  team_values = pd.read_csv('https://raw.githubusercontent.com/A-Peoples/NFL_Play_Predictor/refs/heads/main/datasets/team_values.csv')

  return X_train, X_test, y_train, y_test, team_values

X_train, X_test, y_train, y_test, team_values = load_data()

home_team = st.selectbox("Home Team", team_values['posteam'].unique())
spec_ht = team_values.loc[team_values['posteam'] == home_team]
st.write(str(spec_ht['posteam_num'].iloc[0]))

away_team = st.selectbox("Away Team", team_values['posteam'].unique())
spec_at = team_values.loc[team_values['posteam'] == away_team]
st.write(str(spec_at['posteam_num'].iloc[0]))

quarter = st.selectbox("Minutes in Quarter", range(0, 15))
