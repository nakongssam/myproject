import streamlit as st
st.title('This is my first webapp!!')
txt_data = """
fff
"""

c1, c2 = st.columns((4,1))
with c1:
    with st.expander('Contents'):
        url='https://www.youtube.com/watch?v=s1Qz55ZTxWQ'
        st.video(url)
        st.info('This is left!!')
        st.markdown(txt_data)

with c2:
    with st.expander('Tips..'):
        imglink = 'https://cdn.freezinenews.com/news/photo/202411/2223_2819_4941.jpg'
        st.image(imglink)
        st.info('This ir right!!')

c3, c4 = st.columns((4,1))
with c3:
    with st.expander('Contents'):
        url='https://www.youtube.com/watch?v=s1Qz55ZTxWQ'
        st.video(url)
        st.info('This is left!!')
        st.markdown(txt_data)

with c4:
    with st.expander('Tips..'):
        imglink = 'https://cdn.freezinenews.com/news/photo/202411/2223_2819_4941.jpg'
        st.image(imglink)
        st.info('This ir right!!')