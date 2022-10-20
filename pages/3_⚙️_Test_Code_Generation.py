from code_translator import *
import streamlit as st


if __name__ == '__main__':
    st.write(
        """<style>
        [data-testid="stSidebar"] [data-testid="stImage"] {
            margin-top: 250px;
        }
        svg {
            margin: 0 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    cols = st.sidebar.columns(3)
    cols[0].write('')
    cols[1].image('images/logo_bw.png')
    cols[2].write('')

    st.sidebar.markdown(
        '<h2 style="text-align: center; color: grey; font-family: \'Roboto Condensed\' sans-serif;"><i>Python Code Translator</i></h2>',
        unsafe_allow_html=True)
    st.sidebar.markdown(
        '<p style="text-align: center; color: #aaaaaa; font-family: \'Roboto Condensed\' sans-serif;"><i><br>Junwon Hwang</i></p>\n',
        unsafe_allow_html=True)
    st.sidebar.markdown('''
            <div style="display: flex; justify-content: center; align-content: center;">
                <a href="https://github.com/nuxlear">
                    <div><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="grey" class="bi bi-github" viewBox="0 0 16 16">
                            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.012 8.012 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                    </svg></div>
                </a>
                <a href="mailto:nuclear1221@gmail.com">
                    <div><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="grey" class="bi bi-envelope-fill" viewBox="0 0 16 16">
                            <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"/>
                    </svg></div>
                </a>
            </div>
            ''', unsafe_allow_html=True)

    test_container = st.container()

    test_container.header('⚙️ Test Code Generation')

    if 'test_input' not in st.session_state:
        st.session_state.test_input = None
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None

    test_manual = test_container.expander('See Example For Help')
    test_manual.markdown('''
    ### How To Use?

    First, enter your code that you want to be tested. 
    ''')
    test_manual.image('images/test_1.png', 'Sample input code for test code generation. ', use_column_width='auto')
    test_manual.markdown('''
    After that, you only need to click the **"Generate Test Code"** below!
    ''')
    test_manual.image('images/test_2.png', use_column_width='auto')
    test_manual.markdown('''
    In a minute, the result code samples appear to the right side. 
    ''')
    test_manual.image('images/test_3.png', 'Sample output test code. The result can be different from yours. ', use_column_width='auto')
    test_manual.markdown('''
    The result code may not be valid to execute immediately. 
    
    You may need to re-implement an appropriate test code with the result code you selected. 
    ''')


    msg_bar = test_container.empty()
    test_ui = test_container.container()
    input_cols, output_cols = test_ui.columns(2, gap='medium')

    test_input_form = input_cols.form(key='testcode_input')
    with test_input_form:
        test_input = test_input_form.text_area('Enter the code', value=st.session_state.test_input or '',
                                               height=500, key='test_input_code')
        test_button = test_input_form.form_submit_button('Generate Test Code')

    output_container = output_cols.container()

    output_container.write('Results')
    output_results = output_container.empty()

    if test_button or st.session_state.test_input is not None:
        if test_input not in [st.session_state.test_input, '']:
            st.session_state.test_results = None
        st.session_state.test_input = code = test_input

        if code == '':
            msg_bar.warning('The entered text is empty. ')

        elif st.session_state.test_results is None:
            with output_results:
                with st.spinner('Generating...'):
                    res = get_test_code(code)

            if len(res) == 0:
                msg_bar.error('No results found...', icon='⚠️')
                output_results.code('No Results. \n\nTry another code or Retry it. ', language='markdown')
            else:
                st.session_state.test_results = res

        if st.session_state.test_results is not None:
            res = st.session_state.test_results

            msg_bar.success('Success!', icon='✅')
            output_list = output_results.container()
            for i, gen in enumerate(res):
                gen_box = output_list.expander(f'Test Code #{i+1}', expanded=True)
                gen_box.code(gen, language='python')
