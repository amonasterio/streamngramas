import streamlit as st
import pandas as pd 
import collections
import nltk 
import numpy as np

#Devolvemos el volumen de cada n-grama
def GetVolume(query):
    df_out= df[df['query'].str.contains(query)]
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

ngramas=st.number_input(min_value=2,max_value=6,value=2,label='Seleccione n-gramas (número de palabras agrupadas)')
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
    top=counts.most_common(2000)
    x = pd.DataFrame(top, columns=['query','count'])
    
    #Aplicamos funciones para eliminar caracteres innecsarios y obtener el volumen
    x['query'] = x['query'].apply(RemoveUselessChar)
    x['query'] = x['query'].str.replace(',','')
    x['Volume'] = x['query'].apply(GetVolume)
    st.download_button(
                label="Descargar como CSV",
                data=x.to_csv(index = False).encode('utf-8'),
                file_name='salida.csv',
                mime='text/csv',
            )
    st.dataframe(x)