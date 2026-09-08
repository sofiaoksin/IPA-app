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

with st.bottom:
    st.caption("The audio clips are the work of Peter Isotalo and User:Denelson83. They are "
                "available under a free and/or copyleft licence through [Wikimedia Commons' "
                "General Phonetics collection](https://commons.wikimedia.org/wiki/General_phonetics).")

pg = st.navigation(pages)
pg.run()