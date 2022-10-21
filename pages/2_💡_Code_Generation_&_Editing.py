from code_translator import *
import streamlit as st
import streamlit_nested_layout


if __name__ == '__main__':
    st.set_page_config(
        page_title='Python Code Translator - Code Generation & Editing',
        layout='wide'
    )

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
    st.sidebar.markdown('''
        <div style="display: flex; justify-content: center; align-content: center; margin-top:80px;">
            <a href="https://forms.gle/E2fvoVwEZgMyGUJXA">
                <p style="text-align: center; color: #65afc5; font-family: \'Roboto Condensed\' sans-serif;">Contact Us</p>
            </a>
        </div>
        ''', unsafe_allow_html=True)

    gen_container = st.container()

    gen_container.header('💡 Code Generation & Editing')

    if 'gen_input' not in st.session_state:
        st.session_state.gen_input = None
    if 'gen_results' not in st.session_state:
        st.session_state.gen_results = None
    if 'is_context_expand' not in st.session_state:
        st.session_state.is_context_expand = False

    gen_manual = gen_container.expander('See Example For Help')
    cols = gen_manual.columns(2)
    cols[0].markdown('''
    ### How To Use?
    
    1) For code generation, first enter your description of what you want to generate. 
    
    The description can be short or long enough, but try not exceeding **20 lines**. 
    ''')
    cols[1].image('images/gen_1.png', 'Sample input description for code generation', use_column_width='auto')

    cols = gen_manual.columns(2)
    cols[0].markdown('''
    After that, click the **Generate Code** button below to generate the code. 
    ''')
    cols[1].image('images/gen_2.png', use_column_width='auto')

    cols = gen_manual.columns(2)
    cols[0].markdown('''
    2) If you want to modify your code, you can expand the code input menu, and enter your code. 
    ''')
    cols[1].image('images/gen_3_1.png', use_column_width='auto')

    cols = gen_manual.columns(2)
    cols[0].markdown('''
    Then, click the **Generate Code** button below as same as the code generation. 
    
    The application will automatically choose the code generation/editing by checking whether the code is given. 
    ''')

    cols = gen_manual.columns(2)
    cols[0].markdown('''
    When the model finishes the job, the generated/edited code samples appear on the right side. 
    
    The result code might be different from your intent, or sometimes invalid, so you can choose the proper code from the samples. 
    ''')
    cols[1].image('images/gen_5_1.png', 'Sample output code. The result can be different from yours. ', use_column_width='auto')

    cols = gen_manual.columns(2)
    cols[0].markdown('''
    👉 If you didn't get an appropriate results, you may need to change your description or just retry it!
    
    The results can vary according to your input and trials. 
    ''')

    cols = gen_manual.columns(2)
    cols[0].markdown('''
    You can also click the reaction buttons below each result box for giving your feedback. 
    ''')
    cols[1].image('images/feedback.png', use_column_width='auto')

    msg_bar = gen_container.empty()
    gen_ui = gen_container.container()
    input_cols, output_cols = gen_ui.columns(2, gap='medium')

    gen_input_form = input_cols.form(key='generate_input')
    with gen_input_form:
        gen_context_container = gen_input_form.expander('👉 Click here to edit your code',
                                                        expanded=st.session_state.is_context_expand)
        gen_context_code = gen_context_container.text_area('Enter your code for editing',
                                                           value=st.session_state.gen_input[0] if st.session_state.gen_input else '',
                                                           height=500, key='gen_input_code')
        gen_query = gen_input_form.text_area('Explain your code, or Explain the differences you want to change',
                                             value=st.session_state.gen_input[1] if st.session_state.gen_input else '',
                                             height=200, key='gen_input_query')
        gen_button = gen_input_form.form_submit_button('Generate Code')

    output_container = output_cols.container()

    output_container.write('Results')
    output_results = output_container.empty()

    if gen_button or st.session_state.gen_input is not None:
        if (gen_context_code, gen_query) != st.session_state.gen_input and gen_query != '':
            st.session_state.gen_results = None
        if gen_context_code != '':
            st.session_state.is_context_expand = True
        st.session_state.gen_input = (code, query) = (gen_context_code, gen_query)
        print(st.session_state.gen_input)

        if query == '':
            msg_bar.warning('The entered text is empty. ')

        elif st.session_state.gen_results is None:
            with output_container:
                with st.spinner('Generating...'):
                    if code == '':
                        res, orms = get_generation(query, return_orms=True)
                    else:
                        res, orms = get_modification(code, query, return_orms=True)

            if len(res) == 0:
                msg_bar.error('No results found...', icon='⚠️')
                output_results.code('No Results. Try another query (or code) or Retry it. ', language='markdown')
            else:
                st.session_state.gen_results = (res, orms)

        if st.session_state.gen_results is not None:
            res, orms = st.session_state.gen_results
            infos = [(x.filename, x.input_text, x.output_text) for x in orms]

            msg_bar.success('Success!', icon='✅')
            output_list = output_results.container()
            for i, gen in enumerate(res):
                gen_box = output_list.expander(f'Generated Code #{i+1}', expanded=True)
                gen_box.code(gen, language='python')

                reactions = gen_box.columns([1, 1, 5])
                good_btn = reactions[0].button('👍', key=f'exp_good_{i}')
                bad_btn = reactions[1].button('👎', key=f'exp_bad_{i}')

                if good_btn:
                    update_reaction(*infos[i], 'generate', 'good')
                    reactions[2].success('Thank you for your feedback! "👍"')
                if bad_btn:
                    update_reaction(*infos[i], 'generate', 'bad')
                    reactions[2].error('Thank you for your feedback! "👎"')
