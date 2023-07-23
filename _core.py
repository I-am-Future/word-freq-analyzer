import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

REMOVED_WORD = []
# Preposition and postposition
REMOVED_WORD.extend(['aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'amid', 'among', 'anti', 'around', 'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'besides', 'between', 'beyond', 'but', 'by', 'concerning', 'considering', 'despite', 'down', 'during', 'except', 'excepting', 'excluding', 'following', 'for', 'from', 'in', 'inside', 'into', 'like', 'minus', 'near', 'of', 'off', 'on', 'onto', 'opposite', 'outside', 'over', 'past', 'per', 'plus', 'regarding', 'round', 'save', 'since', 'than', 'through', 'to', 'toward', 'towards', 'under', 'underneath', 'unlike', 'until', 'up', 'upon', 'versus', 'via', 'with', 'within', 'without'])
# Conjunction
REMOVED_WORD.extend(['and', 'that', 'but', 'or', 'as', 'if', 'when', 'than', 'because', 'while', 'where', 'after', 'so', 'though', 'since', 'until', 'whether', 'before', 'although', 'nor', 'like', 'once', 'unless', 'now', 'except', 'yet', 'also'])
# Auxiliary words
REMOVED_WORD.extend(['be', 'is', 'are', 'was', 'were', 'being', 'been', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'upon', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'])
# pronoun, including this, that...
REMOVED_WORD.extend(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves'])
REMOVED_WORD.extend(['what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing'])
# number words, zero to ten, thousands, millions, billions, trillions
REMOVED_WORD.extend(['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'thousand', 'million', 'billion', 'trillion'])
# Modal verb
REMOVED_WORD.extend(['can', 'could', 'may', 'might', 'will', 'would', 'shall', 'should', 'must'])

def do_analysis() -> None:
    st.session_state['exported'] = False
    action = getattr(st.session_state, 'action')
    if action == 'Analysis':
        _do_analysis()
    elif action == 'Analysis & Translation':
        _do_analysis()
        _do_translation()

    filterlevel = getattr(st.session_state, 'filterlevel')
    if filterlevel == 'Filter out 介词连词助词':
        filter_result()
    

def _do_analysis() -> None:

    if not st.session_state['user_input']:
        st.warning('Please input your text!')
        st.stop()
    words = st.session_state['user_input'].split()

    # move the punctuation
    words = [word.strip('.,!;:()[]"') for word in words]
    # move the numbers
    words = [word for word in words if not word.isdigit()]

    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    word_freq = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])
    word_freq.index.name = 'Word'
    word_freq = word_freq.sort_values(by='Frequency', ascending=False)

    st.session_state['num_words'] = len(words)
    st.session_state['word_freq'] = word_freq


def _do_translation() -> None:
    if 'word_freq' not in st.session_state:
        do_analysis()
    
    # if it already has "Translation" column, then remove that column.
    if 'Translation' in st.session_state['word_freq'].columns:
        st.session_state['word_freq'].drop(columns=['Translation'], inplace=True)

    # batch apply to save the query time
    all_words = st.session_state['word_freq'].index.tolist()

    try:
        result = GoogleTranslator(source='auto', target='zh-CN').translate('\n'.join(all_words))
    except:
        st.error('Connecting the translation services failed. Please try again.')

    result = result.split('\n')
    # put the result on the first column
    st.session_state['word_freq'].insert(0, 'Translation', result)


def do_analysis_and_translation() -> None:
    do_analysis()
    _do_translation()


def do_download_prep() -> None:
    if 'word_freq' in st.session_state:
        st.session_state['word_freq'].to_excel('test.xlsx', index=True, header=True)
        st.session_state['exported'] = True

def filter_result() -> None:
    # if 'word_freq' in st.session_state and st.session_state['filterlevel'] == 'Filter out 介词连词助词':
        # filter out Prepositional conjunctions and auxiliary words
    if getattr(st.session_state, 'word_freq', None) is not None and getattr(st.session_state, 'filterlevel', None) == 'Filter out 介词连词助词':
        st.session_state['word_freq'] = st.session_state['word_freq'].drop(REMOVED_WORD, axis=0, errors='ignore')
    

