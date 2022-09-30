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
from cyt5_summarizer import t5_summarize
nltk.download('punkt') # one time execution
nltk.download('stopwords')
from labels import MESSAGES

EXAMPLES_DIR = 'app/example_texts_pub'

def get_input_text(option, lang='cy'):
	input_text=''
	if option == MESSAGES[lang][0]:
		example_fname = st.sidebar.selectbox(MESSAGES[lang][1], sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith('cy')]))
		# with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='iso-8859-1') as example_file:
		with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='utf-8') as example_file:
				example_text = example_file.read()
		input_text = st.text_area(MESSAGES[lang][2], example_text, height=300)

	elif option == MESSAGES[lang][3]:
		text = upload_multiple_files(lang=lang)
		input_text = st.text_area(MESSAGES[lang][4], text, height=300)
	else:
		input_text = st.text_area(MESSAGES[lang][5], MESSAGES[lang][6])
	return input_text

# text_rank
def text_rank_summarize(article, ratio):
  return summa_summarizer(article, ratio=ratio)

#------------------ uploading file --------------------
def uploadfile(lang='cy'):
    if lang=='cy':
        uploaded_file = st.file_uploader("Dewiswch ffeil destun")
        return_msg = '<Uwchlwythwch eich ffeil...>'
    else:
        uploaded_file = st.file_uploader("Choose a text file")
        return_msg = '<Please upload your file ...>'
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        # stringio = StringIO(uploaded_file.getvalue().decode("iso-8859-1"))
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
        bytes_data += uploaded_file.read().decode('utf-8') 
    return bytes_data

#----------------------- apps --------------------------
def run_summarizer():
    language = st.sidebar.selectbox('Newid iaith (Change language):', ['Cymraeg', 'English'])
    lang = 'cy' if language == 'Cymraeg' else 'en'
    summarizer_type = st.sidebar.radio(MESSAGES[f'{lang}.summary.type']+':',
                        (f"{MESSAGES[f'{lang}.extractive']} - TextRank", f"{MESSAGES[f'{lang}.abstractive']} - CyT5Small"))
    if summarizer_type in ['Extractive - TextRank', 'Echdynnol - TextRank']:
        st.markdown(MESSAGES[f'{lang}.ext.md'])
        with st.expander(MESSAGES[f'{lang}.info.title'], expanded=False):
            st.markdown(MESSAGES[f'{lang}.md'])
        option = st.sidebar.radio(MESSAGES[lang][7], (MESSAGES[lang][8], MESSAGES[lang][9], MESSAGES[lang][10]))
        input_text = get_input_text(option, lang=lang)
        chosen_ratio = st.sidebar.slider(MESSAGES[f'{lang}.sb.sl'], min_value=10, max_value=50, step=10, value=40)/100

        if st.button(MESSAGES[f'{lang}.button']):
            if input_text and input_text!='<Rhowch eich testun (Please enter your text...)>':
                summary = text_rank_summarize(input_text, ratio=chosen_ratio)
                if summary:
                    st.write(text_rank_summarize(input_text, ratio=chosen_ratio))
                else:
                    st.write(sent_tokenize(text_rank_summarize(input_text, ratio=0.5))[0])
            else:
                st.info(f"""Rhowch eich testun...(Please enter your text...)""", icon='😎')

    else: # Abstractive Summarizer
        st.markdown(MESSAGES[f'{lang}.abs.md'])
        with st.expander(MESSAGES[f'{lang}.info.title'], expanded=False):
            st.markdown(MESSAGES[f'{lang}.md'])
        
        option = st.sidebar.radio(MESSAGES[lang][7], (MESSAGES[lang][8], MESSAGES[lang][9], MESSAGES[lang][10]))
        input_text = get_input_text(option, lang=lang)
        if st.button(MESSAGES[f'{lang}.button']):
            st.warning(MESSAGES[f'{lang}.abs.warning'])
            if input_text and input_text not in ['<Please enter your text...>','<Please upload your file ...>']:
                summary = t5_summarize('ignatius/cyT5-small', input_text)
                if summary:
                    st.write(summary)
                else:
                    st.write("Well, this should not happen.")
            else:
              st.write('Please select an example, or paste/upload your text')