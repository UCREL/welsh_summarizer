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

EXAMPLES_DIR = 'example_texts_pub'


## Define summarizer models
# text_rank
def text_rank_summarize(article, ratio):
  return summa_summarizer(article, ratio=ratio)

#helper functions---------------------------------------------------

#------------------------- uploading file ---------------------------
def uploadfile():
    uploaded_file = st.file_uploader("Choose a text file")
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        return stringio.read()
    else:
        return '<Please upload your file ...>'

#-----------Get Top n most_common words plus counts--------
@st.cache
def getTopNWords(t, n=5):
    t = [w for w in t.lower().split() if (w not in STOPWORDS and w not in PUNCS)]
    return Counter(t).most_common(n)
    # return [f"{w} ({c})" for w, c in Counter(t).most_common(n)]


#------------------------ keyword in context ------------------------
@st.cache
def get_kwic(text, keyword, window_size=1, maxInstances=10, lower_case=False):
    text = text.translate(text.maketrans("", "", string.punctuation))
    if lower_case:
        text = text.lower()
        keyword = keyword.lower()
    kwic_insts = []
    tokens = text.split()
    keyword_indexes = [i for i in range(len(tokens)) if tokens[i].lower() ==keyword.lower()]
    for index in keyword_indexes[:maxInstances]:
        left_context = ' '.join(tokens[index-window_size:index])
        target_word = tokens[index]
        right_context = ' '.join(tokens[index+1:index+window_size+1])
        kwic_insts.append((left_context, target_word, right_context))
    return kwic_insts

#-------------------------- N-gram Generator ---------------------------
@st.cache
def gen_ngram(text, n=2, top=10):
    _ngrams=[]
    if n==1:
        return getTopNWords(text, top)
    for sent in sent_tokenize(text):
        for char in sent:
            if char in PUNCS: sent = sent.replace(char, "")
        _ngrams += ngrams(word_tokenize(sent),n)
    return [(f"{' '.join(ng):>27s}", c) 
            for ng, c in Counter(_ngrams).most_common(top)]

#apps------------------------------------------------------------------
def run_summarizer():
    language = st.sidebar.selectbox('Newid iaith (Change language):', ['Cymraeg', 'English'])
    with st.expander("ℹ️ - About this app", expanded=False):
        st.markdown(
            """     
            -   This tool adapts the app from the [Welsh Summarization] (https://github.com/UCREL/welsh-summarization-dataset) project!
            -   It performs simple extractive summarisation with the [TextRank]() alrogithm.
            """
        )

    if language=='Cymraeg':
        # st.markdown('### 🌷 Adnodd Creu Crynodebau')
        st.markdown("#### Rhowch eich testun isod:")
        option = st.sidebar.radio('Sut ydych chi am fewnbynnu eich testun?', ('Defnyddiwch destun enghreifftiol', 'Rhowch eich testun eich hun', 'Llwythwch ffeil testun i fyny'))
        
        if option == 'Defnyddiwch destun enghreifftiol':
           st.write(" ".join(os.listdir()))
           example_fname = st.sidebar.selectbox('Select example text:', sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith(('cy','ex'))]))

           with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='utf8') as example_file:
               example_text = example_file.read()

           input_text = st.text_area('Crynhowch y testun enghreifftiol yn y blwch:', example_text, height=300)
        
        elif option == 'Llwythwch ffeil testun i fyny':
            text = uploadfile()
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
        st.markdown('### 🌷 Welsh Summary Creator')
        st.markdown("#### Enter your text below:")
        option = st.sidebar.radio('How do you want to input your text?', ('Use an example text', 'Paste a copied', 'Upload a text file'))
        if option == 'Use an example text':           
           example_fname = st.sidebar.selectbox('Select example text:', sorted([f for f in os.listdir(EXAMPLES_DIR) if f.startswith(('en','ex'))]))
           with open(os.path.join(EXAMPLES_DIR, example_fname), 'r', encoding='utf8') as example_file:
               example_text = example_file.read()
               input_text = st.text_area('Summarise the example text in the box:', example_text, height=300)
        elif option == 'Upload a text file':
            text = uploadfile()
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
