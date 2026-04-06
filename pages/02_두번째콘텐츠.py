import streamlit as st
st.subheader('두번째 콘텐츠')
import pandas as pd
df_score = pd.read_csv('./score.csv')
st.write(df_score)
df_score['총점'] = df_score['국어'] + df_score['영어'] + df_score['수학']
st.table(df_score)
