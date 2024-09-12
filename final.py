import streamlit as st
import json
import requests
import pandas as pd
import time
params= st.query_params.to_dict()
print(params)
def get_backend_models():
    url = 'https://cr-lab-qdrant-5xoqaolxlq-uc.a.run.app/model/get_all'
    datos = {
        "domain": params.get("domain","intercorp.com.pe"),
    }
    respuesta = requests.post(url, json=datos)
    respuesta= respuesta.json()
    return respuesta["data"]

backend_models= get_backend_models()
backend_models_names= [obj['name'] for obj in backend_models]

def send_message(prompt):
    url = st.session_state['backend_url']
    datos = {
        "question": prompt
    }
    encabezados = {'token': 'andina-chatbot-wrfkKF1e5fbfEuCg4o1V7Tpk8iKXGCLttRMHXBCLiv'}
    respuesta = requests.post(url, stream=True, json=datos, headers=encabezados)
    respuesta = respuesta.json()
    answer = respuesta.get("answer")
    response = st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.session1.append({"role": "assistant", "content": response})

    if respuesta.get("image_url",None) is not None:
        print(respuesta["image_url"])
        st.image(respuesta["image_url"])
    if respuesta.get("schema_table",None) is not None:
        df = pd.DataFrame(respuesta["schema_table"])
        st.dataframe(df)
    # data=respuesta.json()
    # response=data['answer']
    # if respuesta.status_code == 200:


def handle_stream(prompt):
    url = st.session_state['backend_url']
    datos = {
        "citeReferences": False,
        "metadata": {
            "userId": "testing-izipay",
            "sessionId": "testing-session-cloud-3"
        },
        "typeDatabase": params.get("vectorStore","test123"),
        "question": prompt,
        "typeModel" : model,
        "temperature":  temp,
        #"bot_data": {
        #    "assistant_name": assistant_name,
        #    "assistant_role" : assistant_role,
        #    "company_name": company_name,
        #    "company_activity": company_activity,
        #    "conversation_purpose": conversation_purpose
        #    }
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
                        print("metadata", content)
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
                            #time.sleep(0.02)
                            #print(content, end='', flush=True)
                    else:
                        print(error)
                        errors.append(error)

            except Exception as e:
                print(e)
                errors.append(str(e))
        print("data", response_data)
        #with st.expander("Referencias"):
            #for count, ref in enumerate(response_data.get("citations")):
                #st.write(f"[{count+1}]", ref["page_content"])
                #st.write("Metadata: ", ref["metadata"])
            #st.write("[1]",response_data["citations"]["page_content"])
            #st.write("Metadata: ", response_data["citations"]["metadata"])
        print("dbug",result)
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
def set_backend_url():
    backend_selected= st.session_state['backend_model_selected']
    print("selected",backend_selected)
    ref= next(obj for obj in backend_models if obj['name'] == backend_selected)
    st.session_state['backend_url'] = ref.get("endpoint")
    st.session_state['has_stream'] = ref.get("has_stream",False)
    print(st.session_state['backend_url'])

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

st.title("Playground demos")

with st.sidebar:
    #session = st.selectbox("Sesión/chat", sesiones, key="session", on_change=switch_chat)
    model = st.selectbox("Modelo OPENAI", OPENAI_CHAT_MODELS, key="model")
    temp= st.slider('Temperature', 0.0, 1.0, 0.2)
    backend_model_selected=st.selectbox("Modelo backend",backend_models_names, key="backend_model_selected", on_change=set_backend_url)
    #assistant_name= st.text_input("Nombre del asistente", "UTPBot")
    #assistant_role= st.text_input("Rol del asistente", "Representante informativo")
    #company_name= st.text_input("Nombre de la empresa", "UTP")
    #company_activity= st.text_input("Rubro de la empresa", "Universidad Tecnológica del Perú")
    #conversation_purpose= st.text_input("Propósito de la conversación", 'Brindar información concisa sobre la universidad Tecnológica del Perú.')
#if "session" not in st.session_state:
   # st.session_state["session"] = session
if "backend_url" not in st.session_state:
    st.session_state["backend_url"]=""
if "has_stream" not in st.session_state:
    st.session_state["has_stream"]=False
if "backend_model_selected" not in st.session_state:
    st.session_state["backend_model_selected"]="test"
if "messages" not in st.session_state:
    st.session_state["messages"]=[]
    #if st.session_state["session"]== "sesion 1":
     #   st.session_state.messages = []
    #if st.session_state["session"]== "sesion 2":
     #   st.session_state.messages = [
      #      {"role": "user", "content": "aaaa"},
       #     {"role": "assistant", "content": "sesion2"},
        #]

if "session1" not in st.session_state:
    st.session_state.session1 =[]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



if prompt := st.chat_input("Escribe un mensaje"):
    #st.image( "https://s3-us-west-2.amazonaws.com/uw-s3-cdn/wp-content/uploads/sites/6/2017/11/04133712/waterfall.jpg",width=400)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.session1.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        question = prompt
        #stream=send_message(question)
        if st.session_state["has_stream"]:

            response = st.write_stream(handle_stream(question))
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.session1.append({"role": "assistant", "content": response})
        else:
            answer = send_message(question)



