import streamlit as st
import json
import requests
import uuid
import time
st.set_page_config(page_title="Cinceplanet bot",page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS1GC53b5X0VCsnupZ_407_-C-Og0Z2y_yl8Q&s")
print("running")
def get_user_uuid():
    user_uuid = str(uuid.uuid4())
    return user_uuid

def reset_session():
    st.session_state["messages"] = []
    st.session_state["user_uuid"] = get_user_uuid()

def save_message(metadata):
    url = 'https://dev-ai-chatbot-cineplanet-yutgchy3pa-uc.a.run.app/add_message'
    encabezados = {'token': 'chatpgt-token-xbpr435'}
    respuesta = requests.post(url, stream=True, json=metadata, headers=encabezados)
    return True

def send_message(prompt):
    url = 'https://dev-ai-chatbot-cineplanet-yutgchy3pa-uc.a.run.app/conversation'
    metadata = {
        "userId": "do-user-test-v3",
        "sessionId": st.session_state["user_uuid"],
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
    respuesta["metadata"]= metadata
    save_message(respuesta)

    return respuesta

col1,col2=st.columns([5,3])
with col1:
    st.title("Cineplanet ChatBot")
with col2:
    if st.button("🔄 Reiniciar sesión"):
        reset_session()
#with st.sidebar:
    #st.write("Chatbot Cineplanet")

if "messages" not in st.session_state:
    st.session_state["messages"]=[]
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = get_user_uuid()
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

        response = st.write(answer.get("answer"))
        with st.expander("Referencias"):
            if isinstance(answer.get("citations", []), list):
                for count, ref in enumerate(answer.get("citations", [])):
                    st.write(f"[{count + 1}]", ref.get("page_content"))
                    st.write("Metadata: ", ref.get("metadata"))
    st.session_state.messages.append({"role": "assistant", "content": answer.get("answer")})

