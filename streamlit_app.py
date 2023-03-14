import streamlit as st
from streamlit_option_menu import option_menu
st.set_page_config(page_title="FIT3164 Coral Reef", page_icon=":ocean:")

header = st.container()
# dataset = st.beta_container()
# features = st.beta_container()
# modelTraining = st.beta_container()
with header:
    st.title('Monitoring Health of Coral Reef')

selected = option_menu(
    menu_title = None,
    options = ["Home","Chatbot","About Us", "Contact Us"],
    icons = ["house","robot","info-circle","telephone-fill"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Home":
    st.title(f"You have selected {selected}")
elif selected == "Chatbot":
    st.title(f"You have selected {selected}")
elif selected == "About Us":
    st.title(f"About Us")
    st.markdown('<div style="text-align: justify;">We are a group of final year university student studying Bachelors of Computer Science majoring in data science. This is our final year group project and the aim of this website is to create a platform for people to view the health of coral reefs to raise awareness about the endangered species of coral reef.</div>', unsafe_allow_html=True)
elif selected == "Contact Us":
    st.title(f"You have selected {selected}")
