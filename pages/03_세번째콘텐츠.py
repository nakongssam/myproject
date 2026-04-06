import streamlit as st
st.subheader('세번째 콘텐츠')

name = st.text_input('Name:')
age = st.number_input('Age:', min_value=1, maxvalue=100, step=1)
email = st.text_input('Email:')

if st.button('방명록에 추가하기'):
    if all ([name,age,email]):
        input_data=f'{name},{age},{email}\n'
        with open('./guestbook.csv', 'a') as f:
            f.write(input_data)
            f.close()
    else:
        st.error('모든 값은 필수입니다.')

import pandas as pd
df_guest = pd.read_csv('./guestbook.csv', encoding='cp949')
st.write(df_guest)
