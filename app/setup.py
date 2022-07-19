import os
import string
import nltk
import numpy as np
import pandas as pd
import streamlit as st
import networkx as nx
from PIL import Image
from io import StringIO
from nltk import word_tokenize, sent_tokenize, ngrams
from collections import Counter
from summa.summarizer import summarize as summa_summarizer
nltk.download('punkt') # one time execution
nltk.download('stopwords')

EXAMPLES_DIR = 'app/example_texts_pub'

## Define summarizer models
# text_rank
def text_rank_summarize(article, ratio):
  return summa_summarizer(article, ratio=ratio)

#helper functions---------------------------------------------------

#------------------------- uploading file ---------------------------
def uploadfile(lang='cy'):
    if lang=='cy':
        uploaded_file = st.file_uploader("Dewiswch ffeil destun")
        return_msg = '<Uwchlwythwch eich ffeil...>'
    else:
        uploaded_file = st.file_uploader("Choose a text file")
        return_msg = '<Please upload your file ...>'
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()
    else:
        return return_msg

def upload_multiple_files(lang='cy'):
    if lang=='cy':
        uploaded_files = st.file_uploader("Dewiswch ffeil destun", accept_multiple_files=True)
        return_msg = '<Uwchlwythwch eich ffeil...>'
    else:
        uploaded_files = st.file_uploader("Select file(s) to upload", accept_multiple_files=True)
        return_msg = '<Please upload your file ...>'
    bytes_data = ''
    for uploaded_file in uploaded_files:
        bytes_data += uploaded_file.read().decode("utf-8") 
    return bytes_data

#apps------------------------------------------------------------------
def run_summarizer():
    language = st.sidebar.selectbox('Newid iaith (Change language):', ['Cymraeg', 'English'])
    if language=='Cymraeg':
        # st.markdown('### 🌷 Adnodd Creu Crynodebau')
        with st.expander("ℹ️ - Gwybodaeth am yr ap hwn", expanded=False):
            st.markdown(
                """
                - Mae’r adnodd hwn yn rhan o brosiect [Adnodd Creu Crynodebau](https://corcencc.org/acc/) (ACC)!
                - Mae’n cynhyrchu crynodeb echdynnol syml gan ddefnyddio algorithm  [TextRank](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf).
                - Mae’r set ddata ar gael drwy [GitHub](https://github.com/UCREL/welsh-summarization-dataset).
                """
            )

        st.sidebar.markdown('### 🌷 Adnodd Creu Crynodebau')
        # st.markdown("#### Rhowch eich testun isod:")
        option = st.sidebar.radio('Sut ydych chi am fewnbynnu eich testun?', ('Defnyddiwch destun enghreifftiol', 'Rhowch eich testun eich hun', 'Uwchlwythwch ffeil destun'))
        
        if option == 'Defnyddiwch destun enghreifftiol':
           example_fname = st.sidebar.selectbox('Select example text:', sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('cy')]))

           with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='utf8') as example_file:
               example_text = example_file.read()

           input_text = st.text_area('Crynhowch y testun enghreifftiol yn y blwch:', example_text, height=300)
        
        elif option == 'Uwchlwythwch ffeil destun':
            text = upload_multiple_files()
            input_text = st.text_area("Crynhoi testun wedi'i uwchlwytho:", text, height=300)

        else:
            input_text = st.text_area('Teipiwch neu gludwch eich testun yn y blwch testun', '<Rhowch eich testun...>')

        chosen_ratio = st.sidebar.slider('Dewiswch gymhareb y crynodeb [10% i 50%]:', min_value=10, max_value=50, step=10)/100
        if st.button("Crynhoi👈"):
            if input_text and input_text!='<Rhowch eich testun (Please enter your text...)>':
                summary = text_rank_summarize(input_text, ratio=chosen_ratio)
                if summary:
                    st.write(text_rank_summarize(input_text, ratio=chosen_ratio))
                else:
                    st.write(sent_tokenize(text_rank_summarize(input_text, ratio=0.5))[0])
            else:
                st.write("Rhowch eich testun...(Please enter your text...)")

    else: #English
        with st.expander("ℹ️ - About this app", expanded=False):
            st.markdown(
                """
                - This tool is part of the [Welsh Summarization Creator](https://corcencc.org/acc/) (WSC) project!
                - It performs simple extractive summarisation with the [TextRank](https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf) algorithm.
                - The dataset is available through [GitHub](https://github.com/UCREL/welsh-summarization-dataset).
                """
            )
        st.sidebar.markdown('### 🌷 Welsh Summary Creator')
        option = st.sidebar.radio('How do you want to input your text?', ('Use an example text', 'Paste a copied', 'Upload a text file'))
        if option == 'Use an example text':           
           example_fname = st.sidebar.selectbox('Select example text:', sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('cy')]))
           with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='utf8') as example_file:
               example_text = example_file.read()
               input_text = st.text_area('Summarise the example text in the box:', example_text, height=300)
        elif option == 'Upload a text file':
            text = upload_multiple_files(lang='en')
            input_text = st.text_area('Summarise uploaded text:', text, height=300)
        else:
            input_text = st.text_area('Type or paste your text into the text box:', '<Please enter your text...>', height=300)

        chosen_ratio = st.sidebar.slider('Select summary ratio [10% to 50%]',  min_value=10, max_value=50, step=10)/100
        if st.button("Summarise👈"):
            if input_text and input_text not in ['<Please enter your text...>','<Please upload your file ...>']:
                summary = text_rank_summarize(input_text, ratio=chosen_ratio)
                if summary:
                    st.write(text_rank_summarize(input_text, ratio=chosen_ratio))
                else:
                    st.write(sent_tokenize(text_rank_summarize(input_text, ratio=0.5))[0])
            else:
              st.write('Please select an example, or paste/upload your text')
        
        summarizer_type = st.sidebar.radio('Summarizer type:', ('Extractive - TextRank', 'Abstractive - CyT5Small'))