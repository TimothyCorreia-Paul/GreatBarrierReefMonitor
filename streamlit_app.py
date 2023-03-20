# Import Libraries
import streamlit as st
import datetime
from streamlit_option_menu import option_menu
from streamlit_chat import message
from PIL import Image
import pandas as pd
import openai
import os

def chatbot_page():
    def predict(message_history):
        # tokenize the new input sentence
        # message_history.append({"role": "user", "content": f"{input}"})

        completion = openai.ChatCompletion.create(
        model="gpt-4", #10x cheaper than davinci, and better. $0.002 per 1k tokens
        messages=message_history
        )
        reply_content = completion['choices'][0]['message']['content']
        # message_history.append({"role": "assistant", "content": f"{reply_content}"}) 
        
        # return message_history, reply_content
        return message_history, reply_content
    
    st.title(f"You have selected {selected}")
    st.title("GPT4 Assistant 🤖 Ask Me Anything!")

    # message_history = [{"role": "system", "content": "You are a helpful assistant. You are an expert in the subject matter of the conversation, namely all matters relating to marine ecosystems around the world. I will specify the subject matter in my messages, and you will reply with a helpful answer that includes the subjects I mention in my messages. Reply only with helpful answers to further input."}]

    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []
    
    if 'message_history' not in st.session_state:
        st.session_state['message_history'] = [{"role": "system", "content": "You are a helpful assistant. You are an expert in the subject matter of the conversation, namely all matters relating to marine ecosystems around the world. I will specify the subject matter in my messages, and you will reply with a helpful answer that includes the subjects I mention in my messages. Reply only with helpful answers to further input."}]

    # user_input = st.text_input("Ask a question!", key="input")

    def get_text():
        input_text = st.text_input("Type here...", key="input")
        return input_text 

    user_input = get_text()

    # message_history = message_history.append({"role": "user", "content": user_input})

    if user_input:
        st.session_state.message_history.append({"role": "user", "content": user_input})
        message_history = st.session_state.message_history
        message_history, reply_content = predict(message_history)
        st.write(st.session_state.message_history)
        st.session_state.message_history.append({"role": "assistant", "content": reply_content})
        st.session_state.past.append(user_input)
        st.session_state.generated.append(reply_content)

    if st.session_state['generated']:
        for i in range(len(st.session_state.message_history)-1, 0, -1):
            message(st.session_state.message_history[i]['choices'][0]['message']['content'], key=str(i))
            message(st.session_state.message_history[i-1]['choices'][0]['message']['content'], is_user=True, key=str(i) + '_user')

        # for i in range(len(st.session_state['generated'])-1, -1, -1):
        #     message(st.session_state["generated"][i], key=str(i))
        #     message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')



# Header creation & page configuration
st.set_page_config(page_title="FIT3164 Coral Reef", page_icon=":ocean:")
header = st.container()
with header:
    st.title('Monitoring Health of Coral Reef')

#Image Assignment
khai = Image.open("khai.png")

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
os.environ["OPENAI_API_KEY"] = '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'
message_history = [{"role": "system", "content": "You are a helpful assistant. You are an expert in the subject matter of the conversation, namely all matters relating to marine ecosystems around the world. I will specify the subject matter in my messages, and you will reply with a helpful answer that includes the subjects I mention in my messages. Reply only with helpful answers to further input."}]

# Home Page
if selected == "Home":
    st.title(f"You have selected {selected}")

# Chatbot Page
elif selected == "Chatbot":
    chatbot_page()

# About Us Page
elif selected == "About Us":
    st.title(f"About Us")
    st.markdown('<div style="text-align: justify;">We are a group of final year university student studying Bachelors of Computer Science majoring in data science. This is our final year group project and the aim of this website is to create a platform for people to view the health of coral reefs to raise awareness about the endangered species of coral reef.</div>', unsafe_allow_html=True)
    
    # Details for Khai Yung
    kycol1, kymid, kycol2 = st.columns([10,1,20])
    with kycol1:
        st.write('')
        st.image(khai, caption="Khai Yung")
    with kycol2:
        st.write('')
        st.write('')
        st.write('Name: Khai Yung Lau')
        st.write('Age: ' + str(year - 2003))
        st.write('Role: Front End Developer')
        st.write('Phone Number: +61468632814')
        st.write('Email: khaiyunglau@gmail.com')

    # Details for Tim
    timcol1, timmid, timcol2 = st.columns([10,1,20])
    with timcol1:
        st.image(khai, caption="Timothy")
    with timcol2:
        st.write('')
        st.write('Name: Timothy')
        st.write('Age: ' + str(year - 2001))
        st.write('Role: ')
        st.write('Phone Number: ')
        st.write('Email: ')

    # Details for ZhouZhou
    zhoucol1, zhoumid, zhoucol2 = st.columns([10,1,20])
    with zhoucol1:
        st.image(khai, caption="Zhou Zhou")
    with zhoucol2:
        st.write('')
        st.write('Name: Zhou')
        st.write('Age: ' + str(year - 2002))
        st.write('Role: ')
        st.write('Phone Number: ')
        st.write('Email: ')

    # Details for JingSeng
    jscol1, jsmid, jscol2 = st.columns([10,1,20])
    with jscol1:
        st.image(khai, caption="Jing Seng")
    with jscol2:
        st.write('')
        st.write('Name: Jing Seng Sin')
        st.write('Age: ' + str(year - 2001))
        st.write('Role: ')
        st.write('Phone Number: +61481169265')
        st.write('Email: ')

# Contact Us Page
elif selected == "Contact Us":
    st.markdown('<h1 style="text-align: center;">Contact Us</h1>',unsafe_allow_html=True)

    # Form to reach out to the team
    with st.form("contact_form", clear_on_submit=True):    
        subject_input = st.text_input('Subject: ')
        email_input = st.text_input('Your Email Address: ')
        name_input = st.text_input('Your Name: ')
        details_input = st.text_area('Details: ')

        submit = st.form_submit_button("Submit")

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
