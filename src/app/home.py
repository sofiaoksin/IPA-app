import streamlit as st

# Title
st.title("🦜 IPA Learning App")

# Optional: Add a header and description
st.header("Welcome to the IPA Learning App")
st.write("Learn International Phonetic Alphabet (IPA) symbols and their pronunciations.")

col1, col2 = st.columns(2)
with col1:
    if st.button("Quiz", width="stretch", icon="🧩"):
        st.switch_page("app/quiz.py")
with col2:
    st.link_button(label="Interactive IPA Chart", url="https://www.ipachart.com", icon="🔬", width="stretch")