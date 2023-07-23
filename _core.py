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

