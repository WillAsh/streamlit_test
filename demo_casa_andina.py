import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import json
import uuid
from datetime import date

st.set_page_config(layout="wide",page_title="Casa Andina BOT",page_icon="https://upload.wikimedia.org/wikipedia/commons/4/48/Logo_Casa_Andina_Hoteles.png")
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")
@st.dialog("Disponibilidad")
def show_modal(text):
    st.write(text)
def print_asd():
    print(wdyn)
def search_docs():
    url = 'https://casa-andina-api-chatbot-v1-yutgchy3pa-uc.a.run.app/search'
    header={
        "token" : "andina-chatbot-wrfkKF1e5fbfEuCg4o1V7Tpk8iKXGCLttRMHXBCLiv"
    }
    datos = {
        "question":wdyn,
    }
    respuesta= requests.post(url, headers=header, json=datos)
    respuesta= json.loads(respuesta.text)
    return respuesta
def view_dispo():
    fecha_inicio, fecha_fin = rango_fechas
    url = 'https://api.aplicacionescasaandina.com:20443/Travelclick/avail'
    datos = {
        "hotelCode": str(hoteles_dict[hotelCode]),
        "dateIn": fecha_inicio.strftime("%Y-%m-%d"),
        "dateOut": fecha_fin.strftime("%Y-%m-%d"),
        "rooms": int(rooms),
        "adults": int(adults),
        "lang": "ES"
    }
    respuesta = requests.post(url, json=datos)
    respuesta = respuesta.text
    show_modal(respuesta)
    print(datos)

def get_user_uuid():
    user_uuid = str(uuid.uuid4())
    return user_uuid

def reset_session():
    st.session_state["messages"] = []
    st.session_state["user_uuid"] = get_user_uuid()
    st.rerun()

def save_message(metadata):
    url = 'https://casa-andina-api-chatbot-v2-yutgchy3pa-uc.a.run.app/add_message'
    encabezados = {'token': 'andina-chatbot-wrfkKF1e5fbfEuCg4o1V7Tpk8iKXGCLttRMHXBCLiv'}
    respuesta = requests.post(url, stream=True, json=metadata, headers=encabezados)
    return True

def send_message(prompt):
    url = 'https://casa-andina-api-chatbot-v2-yutgchy3pa-uc.a.run.app/conversation'
    metadata = {
        "userId": "do-user-test-v3",
        "sessionId": st.session_state["user_uuid"],
        "chatbotId": "fichas-tecnicas",
        # "chatbotId": "e3230312-3fed-4ebc-92ad-6e10e2d0e4bb", # PROD
        "channelType": "WEB"
    }
    datos = {
        "question": prompt,
        "metadata" : metadata
    }
    encabezados = {'token': 'andina-chatbot-wrfkKF1e5fbfEuCg4o1V7Tpk8iKXGCLttRMHXBCLiv'}
    respuesta = requests.post(url, stream=True, json=datos, headers=encabezados)
    respuesta= respuesta.json()
    #print(respuesta)
    respuesta["metadata"] = metadata
    save_message(respuesta)
    return respuesta

archivo_excel = 'hoteles.xlsx'
df = pd.read_excel(archivo_excel)
hoteles_dict = dict(zip(df['Hotel'], df['ID']))

if "messages" not in st.session_state:
    st.session_state["messages"]=[]
if "user_uuid" not in st.session_state:
    st.session_state["user_uuid"] = get_user_uuid()
with st.sidebar:
    st.title("Disponibilidad")
    hotelCode= st.selectbox("Selecciona un hotel", df['Hotel'])
    rango_fechas = st.date_input(
        "Selecciona un rango de fechas",
        value=(date.today(), date.today())  # Valor por defecto
    )
    rooms= st.text_input("Habitaciones",1)
    adults= st.text_input("Adultos",1)
    if st.button("Ver disponibilidad"):
        if not hotelCode:
            st.error("Debes seleccionar un hotel.")
        elif len(rango_fechas) != 2:
            st.error("Debes seleccionar un rango de fechas válido.")
        elif not rooms.isdigit() or int(rooms) <= 0:
            st.error("Ingrese número de habitaciones.")
        elif not adults.isdigit() or int(adults) <= 0:
            st.error("Ingrese número de adultos.")
        else:
            # Si todas las validaciones pasan, ejecuta la función
            view_dispo()



col1, col2 = st.columns([2, 1],)

with col1:
    st.title("Demo casa andina")
    messages = st.container(height=550)

    with messages:
        for message in st.session_state.messages:
            with messages.chat_message(message["role"]):
                st.markdown(message["content"])
    col3,col4 = st.columns([2,9])
    with col3:
        if st.button("🔄 Reiniciar sesión"):
            reset_session()

    with col4:
        if prompt := st.chat_input("Escribe un mensaje"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with messages.chat_message("user"):
                #st.markdown(f"ID:{st.session_state['user_uuid']}")
                st.markdown(prompt)
            with messages.chat_message("assistant"):
                question = prompt
                answer = send_message(question)
                #answer= "xdsadsadsad"
                st.markdown(answer.get("answer"))
                if answer.get("schema_table", None) is not None:
                    df = pd.DataFrame(json.loads(answer["schema_table"]))
                    st.dataframe(df)

                with st.expander("Referencias"):
                    if isinstance(answer.get("citations", []), list):
                        print("exp")
                        for count, ref in enumerate(answer.get("citations", [])):
                            st.write(f"[{count + 1}]", ref.get("page_content"))
                            st.write("Metadata: ", ref.get("metadata"))
                st.session_state.messages.append({"role": "assistant", "content": answer.get("answer")})

with col2:

    if wdyn:= st.text_input("¿Qué necesitas?",key="wdyn"):

        options=search_docs()
        documents = options["documents"]
        documents = [doc for doc in documents if doc["document"]["PUBLIC LINK"] != 'nan'][:3]
        if len(documents) == 0:
            st.write("No se encontraron documentos relacionados")
        else:
            for document in documents[:3]:
                data=document["document"]
                with st.expander(f"{data['TITULO']}",expanded=True):
                    st.write(f"Descripción: {data['DESCRIPCION']}")
                    col_seg,col_keyword = st.columns([5,7])
                    with col_seg:
                        st.write(f"Segmento: {data['SEGMENTO']}")
                    with col_keyword:
                        st.write(f"Keyword: {data['KEYWORD']}")
                    st.markdown(
                        f'<a href="{data["PUBLIC LINK"]}" target="_blank" '
                        f'style="display: inline-block; padding: 0.5rem 1rem; '
                        f'color: white; background-color: #F63366; border: none; '
                        f'border-radius: 5px; text-align: center; text-decoration: none; '
                        f'font-weight: 600; font-size: 16px;">Abrir</a>',
                        unsafe_allow_html=True
                    )
