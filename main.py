# write a single-page website, that there is a text input box.
# The user can input a piece of text, and then we display a 
# word-frequency table and word cloud regarding to the text.

import streamlit as st
import pandas as pd

from _core import (
    do_analysis,
    do_translation,
    do_download_prep
)

# Add website title and favicon
st.set_page_config(page_title='Word Freq Counter Pro', page_icon='📚')

# Title
st.title('Word Frequency Analysis Pro')

# Input box
user_input = st.text_area('Input your text here. We won\'t save your text:', value='', height=200)
user_input = user_input.lower()
st.session_state['user_input'] = user_input

# Buttons
c1, c2, c3 = st.columns(3)
with c1:
    st.button('Analyze', on_click=do_analysis)
with c2:
    st.button('Add translation', on_click=do_translation)
with c3:
    if 'exported' not in st.session_state or not st.session_state['exported']:
        st.button('Export', on_click=do_download_prep)
    else:
        with open('test.xlsx', 'rb') as my_file:
            st.download_button(on_click= do_download_prep, label = 'Download', data = my_file, file_name = 'filename.xlsx')#, mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')     



### Main display ###
if 'word_freq' in st.session_state:
    # First, show the total number of words, total number of distinct words, and distinct ratio here
    st.markdown(f'Total number of words: {st.session_state["num_words"]}, '
                f'total number of distinct words: {len(st.session_state["word_freq"])}, '
                f'distinct ratio: {len(st.session_state["word_freq"])/st.session_state["num_words"]*100:.2f}%')

    # Second, show the table of word frequency
    st.dataframe(st.session_state['word_freq'], use_container_width=True, height=1000)

    



