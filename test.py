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

vs_name=st.query_params["vectorStore"]
vectorstore = get_vectorstore(vs_name)

st.title("Demo chatbot")

with st.sidebar:
    temp= st.slider('Temperature', 0.0, 1.0, 0.2)

if "messages" not in st.session_state:
    st.session_state.messages = []

client = OpenAI(api_key="sk-intercorp-D8GyqPTebT7rMVpUvdo8T3BlbkFJvlPEtwcwjDRUgCEzKihg")


openai_prompt="Actúa como asistente de información, usarás únicamente esta información para tu respuesta: {} para responder a la siguiente petición : {}"
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
        docs_qdrant=[]
        for index,doc in enumerate(retrieval_):
            aux= f'{index+1}. {doc.page_content} \n'
            docs_qdrant.append(aux)
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
        with st.expander("Referencias"):
            for count, ref in enumerate(retrieval_):
                st.write(f"[{count+1}]", ref.page_content)
                st.write("Metadata: ", ref.metadata)

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