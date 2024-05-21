from openai import OpenAI
import streamlit as st
import os
import requests
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

embeddings = OpenAIEmbeddings(model='text-embedding-3-large',openai_api_key="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")

def send_message(prompt):
    url = 'http://127.0.0.1:8000/conversation'
    datos = {
        "citeReferences": True,
        "metadata": {
            "userId": "testing-izipay",
            "sessionId": "testing-session-cloud-3"
        },
        "typeDatabase": "app",
        "question": prompt
    }
    encabezados = {'token': 'my-secret-token'}
    respuesta = requests.post(url, json=datos, headers=encabezados)
    data=respuesta.json()
    response=data['answer']
    if respuesta.status_code == 200:
        print(response)
        return response
        print('La solicitud POST fue exitosa.')
    else:
        print('La solicitud POST falló. Código de estado:', respuesta.status_code)
def switch_chat():
    model_aux= st.session_state['model']
    print("asdasdasd", model_aux)
    if model_aux== "sesion 1":
        st.session_state.messages = [
            {"role": "user", "content": "sesion1 sw"},
            {"role": "assistant", "content": "sesion1 sw"},
        ]
    if model_aux== "sesion 2":
        st.session_state.messages = [
            {"role": "user", "content": "s2"},
            {"role": "assistant", "content": "sesion2"},
        ]
def get_vectorstore(collection: str):
    # embeddings = LLM_EMBEDDINGS()
    client = QdrantClient(
        url="https://ca0a7f3c-a0e4-4810-9b0d-4b3469b6fd86.us-east4-0.gcp.cloud.qdrant.io:6333",
        api_key="cauOrINnZUCDY2CEj2L3d9F0J2P-_rWJimzFQSqDN5Ljq_HKgTNWtA"
    )
    vectorstore = Qdrant(
        client,
        collection_name=collection,
        embeddings=embeddings)
    return vectorstore


vectorstore = get_vectorstore("test123")
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

with st.sidebar:
    session = st.selectbox("Sesión/chat", sesiones, key="model", on_change=switch_chat)
    temp= st.slider('Temperature', 0.0, 1.0, 0.2)

if "session" not in st.session_state:
    st.session_state["session"] = session

if "messages" not in st.session_state:

    if st.session_state["session"]== "sesion 1":
        st.session_state.messages = [
            {"role": "user", "content": "sesion 1"},
            {"role": "assistant", "content": "sesion 1"},
        ]
    if st.session_state["session"]== "sesion 2":
        st.session_state.messages = [
            {"role": "user", "content": "aaaa"},
            {"role": "assistant", "content": "sesion2"},
        ]
client = OpenAI(api_key="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")


openai_prompt="Actúa como asistente de la Universidad Tecnológica del Perú, usarás únicamente esta información para tu respuesta: {} para responder a la siguiente petición : {}"
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
open_ai_array=[]
if prompt := st.chat_input("What is up?"):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        #email = st.query_params["email"]
        #vectorstorea = st.query_params["vectorStore"]
        question = prompt
        response=st.write(send_message(question))

        #retrieval = vectorstore.similarity_search_with_relevance_scores(question, k=5)
        #retrieval_ = [tupla[0] for tupla in retrieval]
        #full_prompt=''
        #for index,doc in enumerate(retrieval_):
            #aux= f'{index+1}. {doc.page_content} \n'
            #full_prompt +=aux
        #print(full_prompt)
        #final_prompt= openai_prompt.format(full_prompt,prompt)
        #open_ai_array.append({"role": "user", "content": final_prompt})
        #response = full_prompt
        #response2 = st.write(response)
        #response= email
        #response2= st.write(response)
        #print(response)


    st.session_state.messages.append({"role": "assistant", "content": response})

asd="""stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in open_ai_array
            ],
            temperature=temp,
            stream=True,
        )
        response = st.write_stream(stream)
        st.button(model)"""