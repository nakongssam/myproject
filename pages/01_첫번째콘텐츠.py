import streamlit as st
st.subheader('첫번째 콘텐츠')

import pandas as pd
df_score = pd.read_csv('./data.csv')
st.write(df)
