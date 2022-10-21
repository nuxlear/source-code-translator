from code_translator import *
import streamlit as st
import streamlit_nested_layout


if __name__ == '__main__':
    st.set_page_config(
        page_title='Python Code Translator - Code Explanation',
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

    exp_container = st.container()

    exp_container.header('💬 Code Explanation')

    if 'exp_input' not in st.session_state:
        st.session_state.exp_input = None
    if 'exp_results' not in st.session_state:
        st.session_state.exp_results = None

    exp_manual = exp_container.expander('See Example For Help')
    cols = exp_manual.columns(2)
    cols[0].markdown('''
    ### How to Use?
    First, Enter your code to input text box on the left side. 
    
    The code must not to be too long, **30-40 lines** are generally okay. 
    ''')
    cols[1].image('images/exp_1.png', 'Sample input code for code explanation', use_column_width='auto')

    cols = exp_manual.columns(2)
    cols[0].markdown('''
    Then click the **"Explain"** Button below. Then the model starts to generate the explanation.
    ''')
    cols[1].image('images/exp_2.png', use_column_width='auto')

    cols = exp_manual.columns(2)
    cols[0].markdown('''
    When the model succeeds to generate the result, the explanation appears on the right side. 
    ''')
    cols[1].image('images/exp_3.png', 'Sample output explanation. The result can be different from yours. ', use_column_width='auto')

    cols = exp_manual.columns(2)
    cols[0].markdown('''
    If there are some vulnerabilities which can be improved, it shows the list of them. 
    ''')
    cols[1].image('images/exp_4.png', use_column_width='auto')

    cols = exp_manual.columns(2)
    cols[0].markdown('''
    Once you click the one of the item, it shows the type of vulnerability and **"Suggest To Fix"** button. 
    
    By clicking the button, the model additionally generates the result code of suggestion 
    which may apply the enhancement point, up to 3 results. 
    
    So, you can choose the result for using freely.  
    
    ''')
    cols[1].image('images/exp_5.png', use_column_width='auto')

    cols = exp_manual.columns(2)
    cols[0].markdown('''
    Moreover, all the results of explanation and suggestion, you can give feedback with clicking button below.
    
    Your feedback makes the model get improved and continuously developed ☺️
    
    ''')
    cols[1].image('images/feedback.png', use_column_width='auto')

    # TODO: Add suggest to fix examples

    msg_bar = exp_container.empty()
    exp_ui = exp_container.container()
    input_cols, output_cols = exp_ui.columns(2, gap='medium')

    exp_input_form = input_cols.form(key='explain_input')
    with exp_input_form:
        exp_input = exp_input_form.text_area('Enter the text', value=st.session_state.exp_input or '', height=500, key='exp_input_text')
        exp_button = exp_input_form.form_submit_button('Explain')

    output_container = output_cols.container()

    output_container.write('Results')
    output_text = output_container.empty()
    output_reaction = output_container.empty()
    suggests = output_container.empty()

    if exp_button or st.session_state.exp_input is not None:
        if exp_input not in [st.session_state.exp_input, '']:
            st.session_state.exp_results = None
        st.session_state.exp_input = code = exp_input

        if code == '':
            msg_bar.warning('The entered text is empty. ')

        elif st.session_state.exp_results is None:
            with output_container:
                with st.spinner('Generating...'):
                    res, orms = get_explanation(code, return_orms=True)

            if len(res) == 0:
                msg_bar.error('No results found...', icon='⚠️')
                output_text.code('No Results. \n\nTry another code or Retry it. ', language='markdown')
            else:
                explanation = res[0]
                orm = orms[0]
                vuls = find_vulnerabilities(code)

                st.session_state.exp_results = (explanation, orm, vuls)

        if st.session_state.exp_results is not None:
            explanation, orm, vuls = st.session_state.exp_results

            msg_bar.success('Success!', icon='✅')
            output_text.markdown(explanation)

            reactions = output_reaction.columns([1, 1, 5])
            good_btn = reactions[0].button('👍', key='exp_good')
            bad_btn = reactions[1].button('👎', key='exp_bad')

            if good_btn:
                update_reaction(orm.filename, orm.input_text, orm.output_text, 'explain', 'good')
                reactions[2].success('Thank you for your feedback! "👍"')
            if bad_btn:
                update_reaction(orm.filename, orm.input_text, orm.output_text, 'explain', 'bad')
                reactions[2].error('Thank you for your feedback! "👎"')

            if 'fix_form' not in st.session_state:
                st.session_state.fix_form = {}

            suggest_container = suggests.container()
            if len(vuls):
                suggest_container.warning(f'There are {len(vuls)} enhancement points on your code. ', icon='💡')
                for i, v in enumerate(vuls):
                    form_key = f'fix_form_{i}'

                    v_content = suggest_container.expander(f'Problem #{i+1}', expanded=True)
                    fix_form = v_content.form(key=form_key)
                    fix_form.markdown(f'**{v["message-id"]} : {v["message"]}**\n\n(Line: {v["line"]})\n\n')
                    fix_button_container = fix_form.empty()
                    fix_button = fix_button_container.form_submit_button('Suggest To Fix')

                    if fix_button or form_key in st.session_state.fix_form:
                        if form_key not in st.session_state.fix_form:
                            st.session_state.fix_form[form_key] = None

                        if st.session_state.fix_form[form_key] is None:
                            with v_content:
                                with st.spinner(''):
                                    _, suggestions, sug_orms = get_enhancements(exp_input, vulnerabilities=[v], return_orms=True)[0]
                                    st.session_state.fix_form[form_key] = (suggestions, sug_orms)

                        if st.session_state.fix_form[form_key] is not None:
                            (suggestions, sug_orms) = st.session_state.fix_form[form_key]
                            for f, (sug, orm) in enumerate(zip(suggestions, sug_orms)):
                                v_content.write(f'Fixed version #{f+1}')
                                v_content.code(sug)
                                sug_reaction = v_content.columns([1, 1, 5])

                                good_btn = sug_reaction[0].button('👍', key=f'sug_{i}_good_{f}')
                                bad_btn = sug_reaction[1].button('👎', key=f'sug_{i}_bad_{f}')

                                if good_btn:
                                    update_reaction(orm.filename, orm.input_text, orm.output_text, 'explain', 'good')
                                    sug_reaction[2].success('Thank you for your feedback! "👍"')
                                if bad_btn:
                                    update_reaction(orm.filename, orm.input_text, orm.output_text, 'explain', 'bad')
                                    sug_reaction[2].error('Thank you for your feedback! "👎"')

                            if len(suggestions) == 0:
                                v_content.error('There is no affordable suggestions. ')

            else:
                suggest_container.info(f'No enhancement points found. ')
