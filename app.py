import streamlit as st


if __name__ == '__main__':
    exp_tab, gen_tab, test_tab = st.tabs(['Explanation', 'Generation', 'Test Code'])

    with exp_tab:
        st.subheader('Code Explanation')
        st.text_area('Enter the text', height=400, key='exp_input')

    with gen_tab:
        st.subheader('Code Generation')
        st.text_area('Enter the text', height=400, key='gen_input')

    with test_tab:
        st.subheader('Test Code Generation')
        st.text_area('Enter the text', height=400, key='test_input')
