from openai import OpenAI
import streamlit as st
import os
import requests
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

embeddings = OpenAIEmbeddings(model='text-embedding-3-large',openai_api_key="sk-intercorp-D8GyqPTebT7rMVpUvdo8T3BlbkFJvlPEtwcwjDRUgCEzKihg")

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
        url="https://2c83a069-f856-4e1d-b84e-a48381264b38.europe-west3-0.gcp.cloud.qdrant.io:6333",
        api_key="4T9h5CAy1zvQ7LUCT15Jfz5_fFvTt7uSd5yBIaWZiKHGDN7jxXY5VA"
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
    #session = st.selectbox("Sesión/chat", sesiones, key="model", on_change=switch_chat)
    temp= st.slider('Temperature', 0.0, 1.0, 0.2)

if "messages" not in st.session_state:
    st.session_state.messages = []

client = OpenAI(api_key="sk-intercorp-D8GyqPTebT7rMVpUvdo8T3BlbkFJvlPEtwcwjDRUgCEzKihg")


openai_prompt="Actúa como asistente de la cadena de hoteles Casa Andina usarás únicamente esta información para tu respuesta: {} para responder a la siguiente petición : {}"
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
        #response=st.write(send_message(question))

        retrieval = vectorstore.similarity_search_with_relevance_scores(question, k=5)
        retrieval_ = [tupla[0] for tupla in retrieval]
        full_prompt=''
        for index,doc in enumerate(retrieval_):
            aux= f'{index+1}. {doc.page_content} \n'
            full_prompt +=aux
        print("prompt:",full_prompt)
        final_prompt= openai_prompt.format(full_prompt,prompt)
        open_ai_array.append({"role": "user", "content": final_prompt})
        response = full_prompt

        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in open_ai_array
            ],
            temperature=temp,
            stream=True,
        )
        response = st.write_stream(stream)

        #response2 = st.write(response)

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