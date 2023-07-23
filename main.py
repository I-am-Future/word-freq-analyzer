# write a single-page website, that there is a text input box.
# The user can input a piece of text, and then we display a 
# word-frequency table and word cloud regarding to the text.

import streamlit as st
import pandas as pd

import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

def do_analysis() -> None:
    st.session_state['translated'] = False
    st.session_state['exported'] = False

    if not st.session_state['user_input']:
        st.warning('Please input your text!')
        st.stop()
    words = st.session_state['user_input'].split()

    # move the punctuation
    words = [word.strip('.,!;:()[]"') for word in words]

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    word_freq = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])
    word_freq.index.name = 'Word'
    word_freq = word_freq.sort_values(by='Frequency', ascending=False)

    st.session_state['translated'] = False
    st.session_state['num_words'] = len(words)
    st.session_state['word_freq'] = word_freq


def do_translation() -> None:
    if 'word_freq' not in st.session_state:
        do_analysis()
    
    st.session_state['translated'] = True

    st.session_state['exported'] = False

    # if it already has "Translation" column, then remove that column.
    if 'Translation' in st.session_state['word_freq'].columns:
        st.session_state['word_freq'].drop(columns=['Translation'], inplace=True)

    # batch apply to save the query time
    all_words = st.session_state['word_freq'].index.tolist()

    result = GoogleTranslator(source='auto', target='zh-CN').translate('\n'.join(all_words))
    result = result.split('\n')
    # put the result on the first column
    st.session_state['word_freq'].insert(0, 'Translation', result)


def do_download_prep() -> None:
    st.session_state['word_freq'].to_excel('test.xlsx', index=True, header=True)
    st.session_state['exported'] = True



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

    



