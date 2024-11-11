import streamlit as st
import pandas as pd
import requests
import json
import os

st.set_page_config(layout="wide")

style_marks = """
<style>
    mark {
        background-color: yellow;
        color: black;
    }
</style>
"""
@st.dialog("Highlights")
def show_modal(text):
    st.markdown(style_marks+text, unsafe_allow_html=True)


sad='''st.markdown("""
    <style>
    .stRadio [role=radiogroup]{
        padding: 10px;
        background-color: #2D2D2D;
        border-radius: 8px;
    }

    </style>
""", unsafe_allow_html=True)'''

def search_docs():
    url = 'https://dev-legal-search-yutgchy3pa-uc.a.run.app/search'
    header={
        "token" : "chatpgt-token-xbpr435"
    }
    datos = {
        "query":query,
        "type_search": search_type
    }
    print("asdxd",search_type)
    respuesta= requests.post(url, headers=header, json=datos)
    respuesta= json.loads(respuesta.text)
    #st.write(respuesta.get("data"))
    #st.markdown(respuesta.get("data")[0]["html_highlights"], unsafe_allow_html=True)
    return respuesta.get("data")


expediente_seleccionado = None
with st.sidebar:
    st.markdown("### Tipo de Búsqueda")

    search_type_mapping = {
        "Por keyword (indexada)": "index",
        "Por Contexto": "vector"

    }
    search_type_visible = st.radio(
        "Seleccione el tipo de búsqueda",
        list(search_type_mapping.keys()),
        index=0,  # Seleccionar la primera opción por defecto
        key="search_type"
    )
    search_type = search_type_mapping[search_type_visible]

    if query := st.text_input("¿Cual es tu consulta?"):

        data = [
            {
                "detalles_caso": {
                    "numero_expediente": "1239-2010 LIMA",
                    "fecha_resolucion": "22/03/2011",
                    "nombre_tribunal": "SALA DE DERECHO CONSTITUCIONAL Y SOCIAL PERMANENTE DE LA CORTE SUPREMA DE JUSTICIA DE LA REPÚBLICA",
                    "ubicacion": "Lima, Perú"
                },
                "partes_involucradas": [
                    {
                        "nombre": "Asociación Country Club El Bosque",
                        "rol": "DEMANDANTE"
                    },
                    {
                        "nombre": "Tribunal Fiscal",
                        "rol": "DEMANDADO"
                    }
                ],
                "representantes_legales": [],
                "leyes": [
                    "Código Tributario",
                    "Ley del Impuesto General a las Ventas",
                    "Reglamento de la Ley del Impuesto General a las Ventas",
                    "Decreto Legislativo N° 821",
                    "Decreto Supremo N° 24-94-EF",
                    "Decreto Supremo N° 130-2005-EF"
                ],
                "articulos": [
                    {
                        "ley": "Código Tributario",
                        "articulo": "IV",
                        "seccion": "Título Preliminar"
                    },
                    {
                        "ley": "Código Tributario",
                        "articulo": "VIII",
                        "seccion": "Título Preliminar"
                    },
                    {
                        "ley": "Decreto Legislativo N° 821",
                        "articulo": "18",
                        "seccion": "inciso b)"
                    },
                    {
                        "ley": "Ley del Impuesto General a las Ventas",
                        "articulo": "23",
                        "seccion": None
                    }
                ],
                "fechas": [
                    {
                        "fecha": "27/08/2009",
                        "descripcion": "Fecha de la sentencia de vista"
                    },
                    {
                        "fecha": "20/05/2008",
                        "descripcion": "Fecha de la sentencia apelada"
                    },
                    {
                        "fecha": "17/08/2010",
                        "descripcion": "Fecha de la resolución que declara procedente el recurso de casación"
                    }
                ],
                "resumen": "La Asociación Country Club El Bosque impugnó una resolución del Tribunal Fiscal que denegó la devolución del IGV pagado en exceso entre 1998 y 2002.  La Corte Suprema declaró fundada la casación, anulando las sentencias anteriores por falta de motivación, al no haberse pronunciado adecuadamente sobre si las cuotas de los asociados constituían operaciones gravadas o no gravadas para efectos del IGV, y la aplicación del procedimiento a prorrata.",
                "resumen_pagina": [
                    {
                        "page": "1",
                        "text": "Se presenta el caso de la Asociación Country Club El Bosque contra el Tribunal Fiscal por la devolución del IGV pagado en exceso. Se declara procedente el recurso de casación por infracción normativa, específicamente la violación del principio de legalidad en materia tributaria y la extensión de disposiciones tributarias a hechos no previstos en la norma."
                    },
                    {
                        "page": "2",
                        "text": "Se detallan los argumentos de la Asociación, incluyendo el Oficio N° 007-2000-K00000 de la SUNAT que indica que las cuotas de los asociados no deben considerarse para el procedimiento a prorrata. Se analiza la aplicación del procedimiento a prorrata y la falta de pronunciamiento de las instancias judiciales sobre los aspectos clave del caso. Se declara nula la sentencia por falta de motivación y se ordena una nueva resolución."
                    }
                ],
                "ideas": [
                    "Infracción del principio de legalidad tributaria.",
                    "Extensión indebida de disposiciones tributarias.",
                    "Aplicación del procedimiento a prorrata para el IGV.",
                    "Naturaleza de las cuotas de los asociados (gravadas o no gravadas).",
                    "Falta de motivación en las sentencias anteriores."
                ],
                "keywords": [
                    "Casación",
                    "IGV",
                    "Impuesto General a las Ventas",
                    "Tribunal Fiscal",
                    "Asociación sin fines de lucro"
                ],
                "reparos": None,
                "nombres": [
                    {
                        "nombre": "Vásquez Cortez",
                        "rol": "Juez"
                    },
                    {
                        "nombre": "Acevedo Mena",
                        "rol": "Juez, Vocal Ponente"
                    },
                    {
                        "nombre": "Yrivarren Fallaque",
                        "rol": "Juez"
                    }
                ],
                "resultado": "Se declara FUNDADO el recurso de casación, NULA la sentencia de vista, e INSUBSISTENTE la sentencia apelada. Se ordena al juez de la causa expedir una nueva resolución.",
                "jueces": [
                    "Vásquez Cortez",
                    "Acevedo Mena",
                    "Yrivarren Fallaque",
                    "Torres Vega",
                    "Cháves Zapater"
                ],
                "asuntos_legales": [
                    "Derecho tributario",
                    "Impuesto General a las Ventas (IGV)",
                    "Principio de legalidad",
                    "Procedimiento a prorrata"
                ],
                "casos_precedentes": [],
                "evidencia": [
                    "Oficio N° 007-2000-K00000 de la SUNAT",
                    "Resolución del Tribunal Fiscal N° 00599-1-2005"
                ],
                "solicitudes": [
                    "Declaración de nulidad de la Resolución del Tribunal Fiscal",
                    "Devolución del IGV pagado en exceso"
                ],
                "fundamentos_legales": [
                    "Violación del principio de legalidad tributaria (artículo IV del Título Preliminar del Código Tributario)",
                    "Extensión indebida de disposiciones tributarias (artículo VIII del Título Preliminar del Código Tributario)",
                    "Falta de motivación en las sentencias (artículo 139 inciso 3) de la Constitución Política del Estado, artículo 122 incisos 3) y 4) del Código Procesal Civil)"
                ],
                "file": {
                    "file_url": "gs://itc-dp-expl-analytics-rcoronado-hciuagvgtn/files-legal/Cas. 1239-2010-Lima.pdf",
                    "file_size": 36903,
                    "num_pages": 2,
                    "public_url": "https://storage.googleapis.com/dev-itcmcand-stg_mlops-chatbot-pb-ghkq/files-legal/Cas.%201239-2010-Lima.pdf"
                },
                "price": {
                    "prompt_token_count": 1269,
                    "candidates_token_count": 1990,
                    "total_token_count": 3259
                }
            },
            {
                "detalles_caso": {
                    "numero_expediente": "1239-2010 LIMA",
                    "fecha_resolucion": "22/03/2011",
                    "nombre_tribunal": "SALA DE DERECHO CONSTITUCIONAL Y SOCIAL PERMANENTE DE LA CORTE SUPREMA DE JUSTICIA DE LA REPÚBLICA",
                    "ubicacion": "Lima, Perú"
                },
                "partes_involucradas": [
                    {
                        "nombre": "Asociación Country Club El Bosque",
                        "rol": "DEMANDANTE"
                    },
                    {
                        "nombre": "Tribunal Fiscal",
                        "rol": "DEMANDADO"
                    }
                ],
                "representantes_legales": [],
                "leyes": [
                    "Código Tributario",
                    "Ley del Impuesto General a las Ventas",
                    "Reglamento de la Ley del Impuesto General a las Ventas",
                    "Decreto Legislativo N° 821",
                    "Decreto Supremo N° 24-94-EF",
                    "Decreto Supremo N° 130-2005-EF"
                ],
                "articulos": [
                    {
                        "ley": "Código Tributario",
                        "articulo": "IV",
                        "seccion": "Título Preliminar"
                    },
                    {
                        "ley": "Código Tributario",
                        "articulo": "VIII",
                        "seccion": "Título Preliminar"
                    },
                    {
                        "ley": "Decreto Legislativo N° 821",
                        "articulo": "18",
                        "seccion": "inciso b)"
                    },
                    {
                        "ley": "Ley del Impuesto General a las Ventas",
                        "articulo": "23",
                        "seccion": None
                    }
                ],
                "fechas": [
                    {
                        "fecha": "27/08/2009",
                        "descripcion": "Fecha de la sentencia de vista"
                    },
                    {
                        "fecha": "20/05/2008",
                        "descripcion": "Fecha de la sentencia apelada"
                    },
                    {
                        "fecha": "17/08/2010",
                        "descripcion": "Fecha de la resolución que declara procedente el recurso de casación"
                    }
                ],
                "resumen": "La Asociación Country Club El Bosque impugnó una resolución del Tribunal Fiscal que denegó la devolución del IGV pagado en exceso entre 1998 y 2002.  La Corte Suprema declaró fundada la casación, anulando las sentencias anteriores por falta de motivación, al no haberse pronunciado adecuadamente sobre si las cuotas de los asociados constituían operaciones gravadas o no gravadas para efectos del IGV, y la aplicación del procedimiento a prorrata.",
                "resumen_pagina": [
                    {
                        "page": "1",
                        "text": "Se presenta el caso de la Asociación Country Club El Bosque contra el Tribunal Fiscal por la devolución del IGV pagado en exceso. Se declara procedente el recurso de casación por infracción normativa, específicamente la violación del principio de legalidad en materia tributaria y la extensión de disposiciones tributarias a hechos no previstos en la norma."
                    },
                    {
                        "page": "2",
                        "text": "Se detallan los argumentos de la Asociación, incluyendo el Oficio N° 007-2000-K00000 de la SUNAT que indica que las cuotas de los asociados no deben considerarse para el procedimiento a prorrata. Se analiza la aplicación del procedimiento a prorrata y la falta de pronunciamiento de las instancias judiciales sobre los aspectos clave del caso. Se declara nula la sentencia por falta de motivación y se ordena una nueva resolución."
                    }
                ],
                "ideas": [
                    "Infracción del principio de legalidad tributaria.",
                    "Extensión indebida de disposiciones tributarias.",
                    "Aplicación del procedimiento a prorrata para el IGV.",
                    "Naturaleza de las cuotas de los asociados (gravadas o no gravadas).",
                    "Falta de motivación en las sentencias anteriores."
                ],
                "keywords": [
                    "Casación",
                    "IGV",
                    "Impuesto General a las Ventas",
                    "Tribunal Fiscal",
                    "Asociación sin fines de lucro"
                ],
                "reparos": None,
                "nombres": [
                    {
                        "nombre": "Vásquez Cortez",
                        "rol": "Juez"
                    },
                    {
                        "nombre": "Acevedo Mena",
                        "rol": "Juez, Vocal Ponente"
                    },
                    {
                        "nombre": "Yrivarren Fallaque",
                        "rol": "Juez"
                    }
                ],
                "resultado": "Se declara FUNDADO el recurso de casación, NULA la sentencia de vista, e INSUBSISTENTE la sentencia apelada. Se ordena al juez de la causa expedir una nueva resolución.",
                "jueces": [
                    "Vásquez Cortez",
                    "Acevedo Mena",
                    "Yrivarren Fallaque",
                    "Torres Vega",
                    "Cháves Zapater"
                ],
                "asuntos_legales": [
                    "Derecho tributario",
                    "Impuesto General a las Ventas (IGV)",
                    "Principio de legalidad",
                    "Procedimiento a prorrata"
                ],
                "casos_precedentes": [],
                "evidencia": [
                    "Oficio N° 007-2000-K00000 de la SUNAT",
                    "Resolución del Tribunal Fiscal N° 00599-1-2005"
                ],
                "solicitudes": [
                    "Declaración de nulidad de la Resolución del Tribunal Fiscal",
                    "Devolución del IGV pagado en exceso"
                ],
                "fundamentos_legales": [
                    "Violación del principio de legalidad tributaria (artículo IV del Título Preliminar del Código Tributario)",
                    "Extensión indebida de disposiciones tributarias (artículo VIII del Título Preliminar del Código Tributario)",
                    "Falta de motivación en las sentencias (artículo 139 inciso 3) de la Constitución Política del Estado, artículo 122 incisos 3) y 4) del Código Procesal Civil)"
                ],
                "file": {
                    "file_url": "gs://itc-dp-expl-analytics-rcoronado-hciuagvgtn/files-legal/Cas. 1239-2010-Lima.pdf",
                    "file_size": 36903,
                    "num_pages": 2,
                    "public_url": "https://storage.googleapis.com/dev-itcmcand-stg_mlops-chatbot-pb-ghkq/files-legal/Cas.%201239-2010-Lima.pdf"
                },
                "price": {
                    "prompt_token_count": 1269,
                    "candidates_token_count": 1990,
                    "total_token_count": 3259
                }
            },
        ]
        data= search_docs()
        for idx, document in enumerate(data[:3]):
            detalles = document["document"]["detalles_caso"]
            with st.expander(f"{detalles['numero_expediente']}", expanded=True):
                st.write(f"Caso: {os.path.splitext(os.path.basename(document['document']['file']['file_uri']))[0]}")
                col_seg, col_keyword = st.columns([5, 7])
                with col_seg:
                    st.write(f"Fecha: {detalles['fecha_resolucion']}")
                with col_keyword:
                    st.write(f"Ubicación: {detalles['ubicacion']}")
                if "highlights" in document:
                    col_abrir,col_highlight,col_link = st.columns([4,5,3])

                    with col_abrir:
                        if st.button(label="Abrir detalles", key=idx):
                            expediente_seleccionado = document["document"]
                    with col_highlight:
                        if st.button(label="Ver coincidencias",key=f"button2_{idx}"):
                            show_modal(document["html_highlights"])
                    with col_link:
                        st.markdown(
                            f'<a href="{document["document"]["file"]["public_url"]}" target="_blank" '
                            f'style="display: inline-flex; padding:0.25rem 0.75rem; '
                            f'color: white; background-color: #2B2C36; border:1px solid rgba(250, 250, 250, 0.2);border-radius:0.5rem;'
                            f' text-align: center; text-decoration: none; height: 1.5rem'
                            f'font-weight: 400; font-size: 1rem;">Ver archivo</a>',
                            unsafe_allow_html=True
                        )
                else:
                    col_abrir,col_link = st.columns([6,6])
                    with col_abrir:
                        if st.button(label="Abrir detalles", key=idx):
                            expediente_seleccionado = document["document"]
                    with col_link:
                        st.markdown(
                            f'<a href="{document["document"]["file"]["public_url"]}" target="_blank" '
                            f'style="display: inline-flex; padding:0.25rem 0.75rem; '
                            f'color: white; background-color: #2B2C36; border:1px solid rgba(250, 250, 250, 0.2);border-radius:0.5rem;'
                            f' text-align: center; text-decoration: none; height: 1.5rem'
                            f'font-weight: 400; font-size: 1rem;">Ver archivo</a>',
                            unsafe_allow_html=True
                        )

if expediente_seleccionado:
    st.header("Detalles del caso", divider=True)
    st.write(f"**Archivo:** {os.path.basename(expediente_seleccionado['file']['file_uri'])} "
             f"**Páginas**: {expediente_seleccionado['file']['num_pages']} "
             f"**Tamaño**: {expediente_seleccionado['file']['file_size'] / (1024 ** 2):.2f} MB "
             f"**Fecha resolución**: {expediente_seleccionado['detalles_caso']['fecha_resolucion']} "
             f"**Tribunal**: {expediente_seleccionado['detalles_caso']['nombre_tribunal']} "
             f"**Ubicación**: {expediente_seleccionado['detalles_caso']['ubicacion']}")
    st.subheader("Resumen")
    st.write(expediente_seleccionado["resumen"])

    chips = "Keywords:"+" ".join([
                         f"<span style='background-color:#3d9df3; border-radius:12px; padding:5px 10px; margin:5px; display:inline-block;'>{text}</span>"
                         for text in expediente_seleccionado["keywords"]])

    # Mostrar en Streamlit como HTML
    st.markdown(chips, unsafe_allow_html=True)

    st.subheader("Resultado")
    st.write(expediente_seleccionado["resultado"])

    st.subheader("Partes involucradas")
    for parte in expediente_seleccionado["partes_involucradas"]:
        st.markdown(f"- {parte.get('nombre')} [{parte.get('rol')}]")

    st.subheader("Jueces")
    for elemento in expediente_seleccionado["jueces"]:
        st.markdown(f"- {elemento}")

    st.subheader("Resumen por página")
    for page in expediente_seleccionado["resumen_pagina"]:
        with st.expander(f"Página {page['page']}"):
            st.write(page["text"])

    st.subheader("Leyes")
    for elemento in expediente_seleccionado["leyes"]:
        st.markdown(f"- {elemento}")


    st.subheader("Fechas")
    df = pd.DataFrame(expediente_seleccionado["fechas"])
    st.dataframe(df,hide_index=True)

    st.subheader("Casos precedentes")
    for elemento in expediente_seleccionado["casos_precedentes"]:
        st.markdown(f"- {elemento}")
