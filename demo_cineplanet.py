import streamlit as st
import json
import requests
import time

def send_message(prompt):
    url = 'https://dev-ai-chatbot-cineplanet-yutgchy3pa-uc.a.run.app/conversation'
    metadata = {
        "userId": "do-user-test-v3",
        "sessionId": "do-session-test-v3",
        "chatbotId": "db_cineplanet",
        # "chatbotId": "e3230312-3fed-4ebc-92ad-6e10e2d0e4bb", # PROD
        "channelType": "WEB"
    }
    datos = {
        "question": prompt,
        "metadata": metadata
    }
    encabezados = {'token': 'chatpgt-token-xbpr435'}
    respuesta = requests.post(url, stream=True, json=datos, headers=encabezados)
    respuesta= respuesta.json()

    return respuesta.get("answer")


st.title("Cineplanet Chatbot")

#with st.sidebar:
    #st.write("Chatbot Cineplanet")

if "messages" not in st.session_state:
    st.session_state["messages"]=[]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe un mensaje"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        question = prompt
        answer= send_message(question)
        response = st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
