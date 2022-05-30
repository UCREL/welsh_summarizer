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

st.sidebar.markdown('## 🌷 Adnodd Creu Crynodebau')

run_summarizer()