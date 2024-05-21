import streamlit as st
import sseclient
import json
import requests
import time


params= st.query_params.to_dict()
print(params)

def send_message(prompt):
    url = 'http://127.0.0.1:8000/conversation_stream'
    datos = {
        "citeReferences": False,
        "metadata": {
            "userId": "testing-izipay",
            "sessionId": "testing-session-cloud-3"
        },
        "typeDatabase": "app",
        "question": prompt
    }
    encabezados = {'token': 'my-secret-token'}
    respuesta = requests.post(url, stream=True, json=datos, headers=encabezados)
    #data=respuesta.json()
    #response=data['answer']
    #if respuesta.status_code == 200:
    return respuesta

def handle_stream(prompt):
    url = 'http://127.0.0.1:8000/conversation_stream'
    datos = {
        "citeReferences": False,
        "metadata": {
            "userId": "testing-izipay",
            "sessionId": "testing-session-cloud-3"
        },
        "typeDatabase": params.get("vectorStore","db_izipay_ecommerce_app_large"),
        "question": prompt,
        "typeModel" : model,
        "temperature":  temp
    }
    encabezados = {'token': 'my-secret-token'}
    errors = []
    response_data = {}
    result = ''
    with requests.post(url, stream=True, json=datos, headers=encabezados) as r:
        for chunk in r.iter_content(2048):
            try:
                block_data = chunk.decode('utf-8')
                content = block_data.split(':', 1)[1].strip()
                if content != '[DONE]':
                    json_data = json.loads(content)
                    success = json_data.get('success')
                    is_metadata = json_data.get('metadata', False)
                    key= json_data.get('key','')
                    key_type = json_data.get('key_type','')
                    error = json_data.get('error', '')
                    if success:
                        content = json_data.get('content')
                        if is_metadata:
                            if key_type == 'list':
                                if not key in response_data:
                                    response_data[key] = []
                                response_data[key].append(content)
                            if key_type == 'dict':
                                if not key in response_data:
                                    response_data[key] = {}
                        else:
                            result += content
                            yield content
                            time.sleep(0.02)
                            #print(content, end='', flush=True)
                    else:
                        print(error)
                        errors.append(error)

            except Exception as e:
                errors.append(str(e))
        print("data",response_data)
        with st.expander("Referencias"):
            for count, ref in enumerate(response_data["citations"]):
                st.write(f"[{count+1}]", ref["page_content"])
                st.write("Metadata: ", ref["metadata"])
            #st.write("[1]",response_data["citations"]["page_content"])
            #st.write("Metadata: ", response_data["citations"]["metadata"])
        return result

session1=[
            {"role": "user", "content": "sesion1 sw"},
            {"role": "assistant", "content": "sesion1 sw"},
        ]
def switch_chat():
    session_aux= st.session_state['session']
    if session_aux== "sesion 1":
        st.session_state.messages = st.session_state.session1
    if session_aux== "sesion 2":
        st.session_state.messages = [
            {"role": "user", "content": "s2"},
            {"role": "assistant", "content": "sesion2"},
        ]

sesiones=(
    "sesion 1",
    "sesion 2"
)
OPENAI_CHAT_MODELS = (
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613",
    "gpt-3.5-turbo-0301",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0613",
    "gpt-4-0314",
    "gpt-4-32k-0314",
)

st.title("Qdrant chat")

#pdf_url = "https://www.buds.com.ua/images/Lorem_ipsum.pdf"

#st.markdown(f'<iframe src="{pdf_url}" width="700" height="500"></iframe>', unsafe_allow_html=True)

with st.sidebar:
    session = st.selectbox("Sesión/chat", sesiones, key="session", on_change=switch_chat)
    model = st.selectbox("Modelo", OPENAI_CHAT_MODELS, key="model")
    temp= st.slider('Temperature', 0.0, 1.0, 0.2)

if "session" not in st.session_state:
    st.session_state["session"] = session

if "messages" not in st.session_state:

    if st.session_state["session"]== "sesion 1":
        st.session_state.messages = []
    if st.session_state["session"]== "sesion 2":
        st.session_state.messages = [
            {"role": "user", "content": "aaaa"},
            {"role": "assistant", "content": "sesion2"},
        ]

if "session1" not in st.session_state:
    st.session_state.session1 =[]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("Escribe un mensaje"):

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.session1.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        question = prompt
        #stream=send_message(question)
        response = st.write_stream(handle_stream(question))

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.session1.append({"role": "assistant", "content":response})
