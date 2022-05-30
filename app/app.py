from setup import *

st.set_page_config(
     page_title='Adnodd Creu Crynodebau (ACC)',
     page_icon='🌷',
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': "https://wp.lancs.ac.uk/acc/",
         'Report a bug': "https://wp.lancs.ac.uk/acc/",
         'About': '''## Welsh Text Summariser.\n This is a demo of the Welsh Summarisation tool!'''
     }
 )

EXAMPLES_DIR = 'example_texts_pub'

# run_summarizer()
language = st.sidebar.selectbox('Newid iaith (Change language):', ['Cymraeg', 'English'])
with st.expander("ℹ️ - About this app", expanded=False):
    st.markdown(
        """     
        - This tool adapts the app from the [Welsh Summarization] (https://github.com/UCREL/welsh-summarization-dataset) project!
        -   It performs simple extractive summarisation with the [TextRank]() alrogithm.
        """
    )

if language=='Cymraeg':
    st.markdown('### 🌷 Adnodd Creu Crynodebau')
    st.markdown("#### Rhowch eich testun isod:")
    option = st.sidebar.radio('Sut ydych chi am fewnbynnu eich testun?', ('Defnyddiwch destun enghreifftiol', 'Rhowch eich testun eich hun', 'Llwythwch ffeil testun i fyny'))
    if option == 'Defnyddiwch destun enghreifftiol':
       example_fname = st.sidebar.selectbox('Select example text:', sorted([f for f in os.listdir(EXAMPLES_DIR)
                                              if f.startswith(('cy','ex'))]))

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
       example_fname = st.sidebar.selectbox('Select example text:', sorted([f for f in os.listdir(EXAMPLES_DIR)
                                              if f.startswith(('en','ex'))]))
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
# language = st.sidebar.selectbox('Newid iaith (Change language):', ['Cymraeg', 'English'])
# if language=='Cymraeg':
     # st.header('🌷 Croeso i’r Adnodd Creu Crynodebau (ACC) f.1.0')
     # st.subheader("Rhowch eich testun isod:")
     
     # option = st.radio(
          # 'Sut ydych chi am fewnbynnu eich testun?',
          # ('Defnyddiwch destun enghreifftiol', 'Rhowch eich testun eich hun'))

     # chosen_ratio = st.sidebar.slider('Dewiswch gymhareb y crynodeb [10% i 50%]:',
                # min_value=10, max_value=50, step=10)/100
                

     # if option == 'Defnyddiwch destun enghreifftiol':
          # input_text = st.text_area('Crynhowch y testun enghreifftiol yn y blwch:', example_text, height=400)
     # else:
          # input_text = st.text_area('Teipiwch neu gludwch eich testun yn y blwch testun', '<Rhowch eich testun...>')

     # if st.button("Crynhoi👈"):
       # if input_text and input_text!='<Rhowch eich testun (Please enter your text...)>':
         # summary = text_rank_summarize(input_text, ratio=chosen_ratio)
         # if summary:
            # st.write(text_rank_summarize(input_text, ratio=chosen_ratio))
         # else:
            # st.write(sent_tokenize(text_rank_summarize(input_text, ratio=0.5))[0])
       # else:
         # st.write("Rhowch eich testun...(Please enter your text...)")
               
# else:
     # st.header('🌷 Welcome to Welsh Text Summary Creator (ACC) v.1.0')
     # st.subheader('Enter your text below:')
     
     # option = st.radio(
          # 'How do you want to input your text?',
          # ('Use example text', 'Enter your own text'))

     # chosen_ratio = st.sidebar.slider('Select summary ratio [10% to 50%]',
                # min_value=10, max_value=50, step=10)/100

     # if option == 'Use example text':
          # input_text = st.text_area('Summarise the example text in the box:', example_text, height=400)
     # else:
          # input_text = st.text_area('Type or paste your text into the text box:', '<Please enter your text...>')
               
     # if st.button("Summarise👈"):
       # if input_text and input_text!='<Please enter your text...>':
         # summary = text_rank_summarize(input_text, ratio=chosen_ratio)
         # if summary:
            # st.write(text_rank_summarize(input_text, ratio=chosen_ratio))
         # else:
            # st.write(sent_tokenize(text_rank_summarize(input_text, ratio=1))[0])
         # # process what needs to be displayed with regards to ratio
       # else:
         # st.write('Please enter your text')
