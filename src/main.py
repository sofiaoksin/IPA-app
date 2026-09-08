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
    st.caption("Each audio clip is the work of Peter Isotalo, " \
    "User:Denelson83, " \
    "and made available under a free and/or copyleft licence. " \
    "For more information, please visit the Wikimedia Commons page for [General Phonetics](https://commons.wikimedia.org/wiki/General_phonetics).")

pg = st.navigation(pages)
pg.run()