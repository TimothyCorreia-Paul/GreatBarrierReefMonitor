# Import Libraries
import streamlit as st
import datetime
from streamlit_option_menu import option_menu
from streamlit_chat import message
from PIL import Image
import pandas as pd
import openai
import os
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def chatbot_page():
    st.title("GPT4 Assistant 🤖 Ask Me Anything!")

    # Setting up session state variables

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    if 'generated_message' not in st.session_state:
        st.session_state['generated_message'] = ""
    
    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = [{"role": "system", "content": "Welcome to The Australian Marine and Coral Reef Ecosystem Monitor! I am your friendly marine ecosystem expert, and I'm here to share my knowledge and passion for the world's coral reefs with you. As an expert on marine coral reef ecosystems, I'm excited to answer your questions and provide you with fascinating insights into the underwater world of corals and marine ecosystems. Whether you're curious about the biodiversity of coral reefs and marine ecosystems, the threats they face, or the conservation efforts underway to protect them, I'm here to help.\nFeel free to ask me anything about marine coral reef ecosystems, including topics such as coral biology, reef ecology, marine species that inhabit coral reefs, and the impact of climate change on these delicate ecosystems. I'm dedicated to keeping our conversation focused on marine ecosystems, so if you have questions on other topics, I may kindly redirect you back to the subject of coral reefs. If asked irrelevant questions, I might reply with 'I don't know' or 'I don't want to answer that', and redirect the conversation back to marine ecosystems.\nTogether, let's explore the vibrant and diverse world of coral reefs and learn how we can contribute to their preservation. Dive in and ask your questions—I'm eager to share my knowledge with you!"}]

    #Loading the chat icons
    user_icon = Image.open('usericon.png')
    openai_icon = Image.open('openaiicon2.png')

    # Function to get user's text input
    def get_text():
        input_text = st.text_input("Type here...", key="input")
        return input_text 
    
    # Setting up the page's user interface
    user_input = get_text() # text box
    st.divider()

    pcol1, pcol2 = st.columns([1, 10]) # Component for the text streaming
    # pcol1.image(openai_icon, width=50)
    plcol2_text = pcol2.empty()

    conversation_history = st.container() # Component for the conversation history

    # Main execution loop, runs when user sends a message, does all the backend stuff.
    if user_input:
        pcol2.empty()
        st.session_state.message_history.append({"role": "user", "content": user_input})
        st.session_state.message_history.append({"role": "assistant", "content": "You sent a new message to quickly for me to respond."})

        # This block of code is for displaying the conversation history
        with conversation_history:
            st.divider()
            for i in range(len(st.session_state.message_history)-2, 0, -2):
                # Display the user messages
                col1, col2 = st.columns([1, 10])
                col1.image(user_icon, width=50)
                col2.markdown(st.session_state.message_history[i]['content'])
                st.divider()
                
                # Don't display the system message
                if i == 1:
                    break

                # Display the AI assistant messages
                col3, col4 = st.columns([1, 10])
                col3.image(openai_icon, width=50)
                col4.markdown(st.session_state.message_history[i-1]['content'])
                st.divider()
        
            # Stream the OpenAI API with message history
            message_history = st.session_state.message_history
            completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", #10x cheaper than davinci, and better. $0.002 per 1k tokens
            messages=message_history,
            stream=True
            )

            # This block of code is for displaying the streaming the AI assistant's response
            with pcol2:
                plcol2_text = pcol2.empty()
                pcol1.image(openai_icon, width=50)
                completion_text = ''
                for chunk in completion:
                    chunk_message = chunk['choices'][0]['delta']
                    keys = chunk_message.keys()
                    if 'content' in keys:
                        completion_text += chunk_message['content']
                        plcol2_text.markdown(completion_text)
                        st.session_state.message_history.pop()
                        st.session_state.message_history.append({"role": "assistant", "content": completion_text})
                
        # This is just for debugging, comment out before we deploy.
        st.write(st.session_state.message_history)

# Header creation & page configuration
st.set_page_config(page_title="FIT3164 The Australian Marine Ecosystem Monitor", page_icon=":ocean:", layout="wide")
header = st.container()
with header:
    st.title('The Australian Marine Ecosystem Monitor')

today = datetime.date.today()
year = today.year

# Navigation bar
selected = option_menu(
    menu_title = None,
    options = ["Home","Chatbot","About Us", "Contact Us"],
    icons = ["house","robot","info-circle","telephone-fill"],
    default_index=0,
    orientation="horizontal",
)

# Setting up the GPT4 chatbot
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Home Page
if selected == "Home":
    tableau_public_embed_code = """
    <div class='tableauPlaceholder' id='viz1679884696848' style='position: relative'><noscript><a href='#'><img alt='Sheet 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Coralmap&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Coralmap&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Co&#47;Coralmap&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1679884696848');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='1000px';vizElement.style.height='1000px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
    """

    st.components.v1.html(tableau_public_embed_code, width=1000, height=1000)

    df = pd.read_csv("Inner.csv")
    st.map(df)

# Chatbot Page
elif selected == "Chatbot":
    chatbot_page()

# About Us Page
elif selected == "About Us":
    st.title(f"About Us")
    st.markdown('<div style="text-align: justify;">We are a group of final year university student studying Bachelors of Computer Science majoring in data science. This is our final year group project and the aim of this website is to create a platform for people to view the health of coral reefs to raise awareness about the endangered species of coral reef.</div>', unsafe_allow_html=True)
    st.write('')
    st.write('')

    st.subheader('Team Members')

    col1, col2 = st.columns([10,10])
    # Details for Khai Yung
    with col1:
        st.write('Name: Khai Yung Lau')
        st.write('Age: ' + str(year - 2003))
        st.write('Email: klau0021@student.monash.edu')
        st.write('Nationality: Malaysian')

    # Details for Tim
    with col2:
        st.write('Name: Timothy Correia-Paul')
        st.write('Age: ' + str(year - 1996))
        st.write('Email: tcor0005@student.monash.edu')
        st.write('Nationality: Australian')

    # Details for ZhouZhou
    with col1:
        st.write('')
        st.write('')
        st.write('Name: Zhou Zhou')
        st.write('Age: ' + str(year - 2001))
        st.write('Email: zzhou0044@student.monash.edu')
        st.write('Nationality: Chinese')

    # Details for JingSeng
    with col2:
        st.write('')
        st.write('')
        st.write('Name: Jing Seng Sin')
        st.write('Age: ' + str(year - 2001))
        st.write('Email: jsin0036@student.monash.edu')
        st.write('Nationality: Malaysian')

    st.subheader('Supervisor from Monash University')
    st.write('Name: Daniel Jitnah')
    st.write('Email: daniel.jitnah@monash.edu')
    st.write('Name: Varun Mathur')
    st.write('Email: varun.mathur@monash.edu')
    st.write('Name: Bhanuka Gamage')
    st.write('Email: bhanuka.gamage@monash.edu')
    
# Contact Us Page
elif selected == "Contact Us":
    st.markdown('<h1 style="text-align: center;">Contact Us</h1>',unsafe_allow_html=True)

    #Validation check for email address
    try:
        with st.form("contact_form", clear_on_submit=True):
            subject_input = st.text_input('Subject: ')
            email_input = st.text_input('Your Email Address: ')
            name_input = st.text_input('Your Name: ')
            details_input = st.text_area('Details: ')

            submit = st.form_submit_button("Submit")

            if check(email_input) == True:
                pass
            elif check(email_input) == False:
                submit = False
                st.error("Please enter a valid Email address")
    except:
        print("invalid email address")
    else:
        df = pd.read_csv('df.csv')
        # When the submit button is pressed, write the input into csv file
        if submit == True:
            inputs = {'subject': [subject_input],
                'email': [email_input],
                'name': [name_input],
                'details': [details_input]           
            }
            df = df.append(inputs, ignore_index = True)
            open('df.csv','w').write(df.to_csv())
            # Respond to the button click
            st.write("Thank you for contacting us, we will reply to your message as soon as possible!")
