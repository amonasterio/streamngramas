import streamlit as st
import pandas as pd 
import collections
import nltk 
import numpy as np

#Devolvemos el volumen de cada n-grama
def GetVolume(query):
    df_out= df[df['query'].str.contains(query,regex=False)]
    return df_out['impressions'].sum()

#Eliminamos caracteres no necesarios
def RemoveUselessChar(x):
    output=''
    for element in x:
        if "'" == element:
            continue
        elif '('==element:
            continue
        elif ')' == element:
            continue
        if "+" == element:
            continue
        if "-" == element:
            continue
        else:
            output+=' '+element
    #Si tiene más de un caracter, eliminamos el primer elemento que será un espacio
    if len(output)>1:
        output=output[1:]
    return output

st.set_page_config(
   page_title="Análisis de N-gramas"
)
st.title("Análisis de N-gramas")
st.text("Devuelve los ngramas de las consultas que les pasemos en el csv extraído de Search Console")
st.text("Condiciones: el csv que le pasemos debe tener los campos 'query' e 'impressions'")
ngramas=st.number_input(min_value=2,max_value=8,value=2,label='Seleccione n-gramas (número de palabras agrupadas)')
max_palabras=st.slider(min_value=1000,max_value=10000,value=4000,step=100,label='Seleccione el número máximo de palabras comunes a extraer')
f_entrada=st.file_uploader('CSV con datos de Search Console', type='csv')


if f_entrada is not None:
    df = pd.read_csv(f_entrada)
    list_of_keywords = df['query'].tolist()
    list_of_words_in_keywords = [x.split(" ") for x in list_of_keywords]
    
    #Variable que almacena el número de veces que aparece un grupo de palabras
    counts = collections.Counter()
    
    #Actualizamos esta variable para comprobar el número de veces que aparece cada n-grama 
    for phrase in list_of_words_in_keywords:
        i=1
        while i <= ngramas:
            counts.update(nltk.ngrams(phrase, i))
            i+=1
    
    #Indicamos el número de palabras más comunes a extraer
    top=counts.most_common(max_palabras)
    x = pd.DataFrame(top, columns=['query','count'])
    
    #Aplicamos funciones para eliminar caracteres innecsarios y obtener el volumen
    x['query'] = x['query'].apply(RemoveUselessChar)
    x['query'] = x['query'].str.replace(',','')
    x['Volume'] = x['query'].apply(GetVolume)
    x['words']= x['query'].str.split(' ').str.len()
    st.dataframe(x.iloc[:,[0,1,2]], height=500)
    st.download_button(
                label="Descargar como CSV (Completo)",
                data=x.to_csv(index = False).encode('utf-8'),
                file_name='salida.csv',
                mime='text/csv',
            )
    
    
    # CSS to inject contained in a string
    hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    j=ngramas
    while j > 0:
        st.subheader(str(j)+" palabras")
        sub=x[x["words"]==j].iloc[:,[0,1,2]].reset_index(drop=True)
        st.dataframe(sub, height=500)
        st.download_button(
                label='Descargar como CSV ('+str(j)+' palabras)',
                data=sub.to_csv(index = False).encode('utf-8'),
                file_name='salida_'+str(j)+'.csv',
                mime='text/csv',
            )
        j-=1
    st.success('Fin')
