from openai import OpenAI
import streamlit as st
import pandas as pd
import uuid
import requests
from streamlit_cookies_manager import EncryptedCookieManager

cookies = EncryptedCookieManager(prefix="test", password="some_secret_password")

if not cookies.ready():
    st.stop()
def get_user_uuid():
    user_uuid = cookies.get('user_uuid')
    if user_uuid:
        return user_uuid
    else:
        user_uuid = str(uuid.uuid4())
        cookies['user_uuid'] = user_uuid
        cookies.save()
        return user_uuid

user_uuid = get_user_uuid()
def get_user_id():
    url = 'http://127.0.0.1:5000/user_sessions/get_user_id'
    datos = {
        "channel_type_id": "streamlit",
        "uuid": user_uuid
    }
    respuesta = requests.post(url, json=datos)
    respuesta = respuesta.json()
    return respuesta["data"]
if "chat_user_uuid" not in st.session_state:
    st.session_state["chat_user_uuid"] = get_user_id().get("chat_user_uuid")

st.write(f"UUID : {user_uuid}")
st.write(f"chat_user_uuid : {st.session_state['chat_user_uuid']}")
#cookies.save()



def send_message(prompt_):
    url = 'http://127.0.0.1:5000/user_sessions/send_message'
    datos = {
        "chat_user_uuid": st.session_state["chat_user_uuid"],
        "chatbot_id": "gpt",
        "channel_type_id": "streamlit",
        "uuid": user_uuid,
        "prompt": prompt_
    }
    respuesta = requests.post(url, json=datos)
    respuesta = respuesta.json()
    respuesta= respuesta["data"]
    session_id= f"session_id: {respuesta['session_id']}"
    st.write(session_id)
    st.session_state.messages.append({"role": "assistant", "content": session_id})
    return respuesta.get("response")

st.title("Demo sesiones")

client = OpenAI(api_key="sk-intercorp-D8GyqPTebT7rMVpUvdo8T3BlbkFJvlPEtwcwjDRUgCEzKihg")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer = send_message(prompt)
        response = st.write(answer)
        print(response)
    st.session_state.messages.append({"role": "assistant", "content": answer})