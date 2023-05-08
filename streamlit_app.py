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
    def predict(message_history):
        # tokenize the new input sentence
        # message_history.append({"role": "user", "content": f"{input}"})

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", #10x cheaper than davinci, and better. $0.002 per 1k tokens
        messages=message_history
        )
        reply_content = completion['choices'][0]['message']['content']
        # message_history.append({"role": "assistant", "content": f"{reply_content}"}) 
        
        # return message_history, reply_content
        return reply_content
    
    st.title("GPT4 Assistant 🤖 Ask Me Anything!")

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    if 'generated_message' not in st.session_state:
        st.session_state['generated_message'] = ""
    
    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = [{"role": "system", "content": "You are a helpful assistant. You are an expert in the subject matter of the conversation, namely all matters relating to marine ecosystems around the world. I will specify the subject matter in my messages, and you will reply with a helpful answer that includes the subjects I mention in my messages. Reply only with helpful answers to further input. Keep the conversation topical to marine ecosystems, and do not stray from the topic. If asked irrelevant questions, you can reply with 'I don't know' or 'I don't want to answer that'."}]

    user_icon = Image.open('usericon.png')
    openai_icon = Image.open('openaiicon2.png')

    def get_text():
        input_text = st.text_input("Type here...", key="input")
        return input_text 

    user_input = get_text()

    st.divider()

    completion_text = ''

    # placeholder_container = st.container()
    pcol1, pcol2 = st.columns([1, 10])
    pcol1.image(openai_icon, width=50)
    plcol2_text = pcol2.empty()

    conversation_history = st.container()

    # if user_input:
    #     st.session_state.message_history.append({"role": "user", "content": user_input})
    #     message_history = st.session_state.message_history
    #     reply_content = predict(message_history)

    #     st.session_state.message_history.append({"role": "assistant", "content": reply_content})
    #     st.session_state.past.append(user_input)
    #     st.session_state.generated.append(reply_content)

    # message(st.session_state.message_history[i]['content'], key="streaming_response")
    # if st.session_state['generated']:
    #     for i in range(len(st.session_state.message_history)-1, 0, -2):
    #         message(st.session_state.message_history[i]['content'], key=str(i))
    #         message(st.session_state.message_history[i-1]['content'], is_user=True, key=str(i) + '_user')
    #     st.write(st.session_state.message_history)

    if user_input:
        pcol2.empty()
        st.session_state.message_history.append({"role": "user", "content": user_input})
        # st.session_state.message_history.append({"role": "user", "content": ""})

        with conversation_history:
            st.divider()
            for i in range(len(st.session_state.message_history)-1, 0, -2):
                col1, col2 = st.columns([1, 10])
                # col1.markdown("**User:**")
                col1.image(user_icon, width=50)
                col2.markdown(st.session_state.message_history[i]['content'])
                st.divider()
                if i == 1:
                    break
                col3, col4 = st.columns([1, 10])
                # col3.markdown("**AI:**")
                col3.image(openai_icon, width=50)
                col4.markdown(st.session_state.message_history[i-1]['content'])
                st.divider()
        
            # Call OpenAI API with message history
            message_history = st.session_state.message_history
            completion = openai.ChatCompletion.create(
            model="gpt-4", #10x cheaper than davinci, and better. $0.002 per 1k tokens
            messages=message_history,
            stream=True
            )

            with pcol2:
                # plcol2_text.markdown("Waiting for a response...")
                plcol2_text = pcol2.empty()
                for chunk in completion:
                    chunk_message = chunk['choices'][0]['delta']
                    keys = chunk_message.keys()
                    if 'content' in keys:
                        completion_text += chunk_message['content']
                        # placeholder_response.markdown(completion_text)
                        plcol2_text.markdown(completion_text)
                        st.session_state.message_history.pop()
                        st.session_state.message_history.append({"role": "assistant", "content": completion_text})
                

        # st.write(st.session_state.message_history)

# Header creation & page configuration
st.set_page_config(page_title="FIT3164 Coral Reef Monitor", page_icon=":ocean:")
header = st.container()
with header:
    st.title('Monitoring Health of Coral Reef')

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
