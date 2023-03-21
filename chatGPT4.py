import gradio as gr
import openai
import os
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from gpt_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper

# openai.api_key = open("key.txt", "r").read().strip("\n")
os.environ["OPENAI_API_KEY"] = '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'

# load from disk
index = GPTSimpleVectorIndex.load_from_disk('index.json')

message_history = [{"role": "system", "content": "You are a helpful assistant. You are an expert in the subject matter of the conversation, namely all matters relating to marine ecosystems around the world. I will specify the subject matter in my messages, and you will reply with a helpful answer that includes the subjects I mention in my messages. Reply only with helpful answers to further input."}]

def GPT4_Response(message_history: list):
    pass

def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    completion = openai.ChatCompletion.create(
      model="gpt-4", #10x cheaper than davinci, and better. $0.002 per 1k tokens
      messages=message_history
    )

    #Just the reply:
    reply_content = completion['choices'][0]['message']['content']
    print(reply_content)

    # To query GPT-Index:
    response = index.query(input)
    # reponse.reponse is the actual response of the index query.
    
    message_history.append({"role": "assistant", "content": f"{reply_content}"+"\n\n"+f"{response.response}"}) 
    # message_history.append({"role": "assistant", "content": f"{response.response}"}) 
    
    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(0, len(message_history), 2)]  # convert to tuples of list
    return response

# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo: 

    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot(value=[("Ask a question or say hello!", "Responses from the assistant will appear here.")]) 

    # creates a new Row component, which is a container for other components.
    with gr.Row(): 
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
    txt.submit(predict, txt, chatbot) # submit(function, input, output)
    #txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string 

    '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
    txt.submit(None, None, txt, _js="() => {''}") # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.
         
demo.launch()