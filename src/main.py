import streamlit as st

# Page configuration
st.set_page_config(
    page_title="IPA Learning App",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = [
    st.Page("app/home.py", title="Home"),
    st.Page("app/quiz.py", title="Quiz"),
]

pg = st.navigation(pages)
pg.run()