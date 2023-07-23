# write a single-page website, that there is a text input box.
# The user can input a piece of text, and then we display a 
# word-frequency table and word cloud regarding to the text.

import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

from _core import (
    do_analysis,
    do_download_prep,
)

# Add website title and favicon
st.set_page_config(page_title='Word Freq Counter Pro', page_icon='📚')

# Title
st.title('Word Frequency Analysis Pro')

st.markdown('''
Quick Guide:
1. Input your text in the box below.

2. Select an action: "Analysis" or "Analysis & Translation" (This will show the Chinese meaning).

3. Select a filter level: "No filter" or "Filter out trivial words" (This will remove words like "as", "the"...).     

4. Press the "Analyze" button.
            
5. Press the "Export" button, then press the "Download" button (This will download an Excel file.)
''')

# Input box
user_input = st.text_area('Input your text here. We won\'t save your text:', value='', height=200)
user_input = user_input.lower()
st.session_state['user_input'] = user_input

st.markdown('Set the following configs first, then press the "Analyze" button! ')

# Select box
c1, c2 = st.columns(2)
with c1:
    st.radio('Select an action:', options=['Analysis', 'Analysis & Translation'], key='action')
with c2:
    st.radio('Select a filter level:', options=['No filter', 'Filter out trivial words'], key='filterlevel')


# Buttons
c1, c2 = st.columns(2)
with c1:
    st.markdown('Translation may take a while.')
    st.button('Analyze', on_click=do_analysis)

with c2:
    st.markdown('Export first, then download.')
    if ('exported' not in st.session_state) or (not st.session_state['exported']):
        st.button('Export', on_click=do_download_prep)
    else:
        with open('test.xlsx', 'rb') as my_file:
            st.download_button(label = 'Ready to Download!', data = my_file, file_name = 'WordFreqCountPro.xlsx')#, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')     



### Main display ###
if 'word_freq' in st.session_state:
    # First, show the total number of words, total number of distinct words, and distinct ratio here
    st.markdown(f'Total number of words: {st.session_state["num_words"]}, '
                f'total number of distinct words: {len(st.session_state["word_freq"])}, '
                f'distinct ratio: {len(st.session_state["word_freq"])/st.session_state["num_words"]*100:.2f}%')

    # Second, show the table of word frequency
    st.dataframe(st.session_state['word_freq'], use_container_width=True, height=1000)

    



