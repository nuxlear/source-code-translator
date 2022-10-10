from code_translator import *
import streamlit as st


if __name__ == '__main__':
    st.set_page_config(layout='wide')

    exp_container = st.container()

    exp_container.header('💬 Code Explanation')

    if 'exp_input' not in st.session_state:
        st.session_state.exp_input = None
    if 'exp_results' not in st.session_state:
        st.session_state.exp_results = None

    exp_manual = exp_container.expander('See Example For Help')
    exp_manual.write('')

    msg_bar = exp_container.empty()
    exp_ui = exp_container.container()
    input_cols, output_cols = exp_ui.columns(2, gap='medium')

    exp_input_form = input_cols.form(key='explain_input')
    with exp_input_form:
        exp_input = exp_input_form.text_area('Enter the text', height=500, key='exp_input_text')
        exp_button = exp_input_form.form_submit_button('Explain')

    output_container = output_cols.container()

    output_container.write('Results')
    output_text = output_container.empty()
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
                    res = get_explanation(code)

            if len(res) == 0:
                msg_bar.error('No results found...', icon='⚠️')
                output_text.code('No Results. \n\nTry another code or Retry it. ', language='markdown')
            else:
                explanation = res[0]
                vuls = find_vulnerabilities(code)

                st.session_state.exp_results = (explanation, vuls)

        if st.session_state.exp_results is not None:
            explanation, vuls = st.session_state.exp_results

            msg_bar.success('Success!', icon='✅')
            output_text.code(explanation, language='python')

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
                                    _, suggestions = get_enhancements(exp_input, vulnerabilities=[v])[0]
                                    st.session_state.fix_form[form_key] = suggestions

                        if st.session_state.fix_form[form_key] is not None:
                            suggestions = st.session_state.fix_form[form_key]
                            for f, sug in enumerate(suggestions):
                                v_content.write(f'Fixed version #{f+1}')
                                v_content.code(sug)

                            if len(suggestions) == 0:
                                v_content.error('There is no affordable suggestions. ')

            else:
                suggest_container.info(f'No enhancement points found. ')
