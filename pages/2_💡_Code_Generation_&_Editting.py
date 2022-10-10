from code_translator import *
import streamlit as st


if __name__ == '__main__':
    gen_container = st.container()

    gen_container.header('💡 Code Generation & Editing')

    if 'gen_input' not in st.session_state:
        st.session_state.gen_input = None
    if 'gen_results' not in st.session_state:
        st.session_state.gen_results = None

    gen_manual = gen_container.expander('See Example For Help')
    gen_manual.write('')

    msg_bar = gen_container.empty()
    gen_ui = gen_container.container()
    input_cols, output_cols = gen_ui.columns(2, gap='medium')

    gen_input_form = input_cols.form(key='generate_input')
    with gen_input_form:
        gen_context_container = gen_input_form.expander('👉 Click here to edit your code')
        gen_context_code = gen_context_container.text_area('Enter your code for editting', height=500, key='gen_input_code')
        gen_query = gen_input_form.text_area('Explain your code, or Explain the differences you want to change',
                                             height=200, key='gen_input_query')
        gen_button = gen_input_form.form_submit_button('Generate Code')

    output_container = output_cols.container()

    output_container.write('Results')
    output_results = output_container.empty()

    if gen_button or st.session_state.gen_input is not None:
        if (gen_context_code, gen_query) != st.session_state.gen_input and gen_query != '':
            st.session_state.gen_results = None
        st.session_state.gen_input = (code, query) = (gen_context_code, gen_query)

        if query == '':
            msg_bar.warning('The entered text is empty. ')

        elif st.session_state.gen_results is None:
            if code == '':
                res = get_generation(query)
            else:
                res = get_modification(code, query)

            if len(res) == 0:
                msg_bar.error('No results found...', icon='⚠️')
                output_results.code('No Results. Try another query (or code) or Retry it. ', language='markdown')
            else:
                st.session_state.gen_results = res

        if st.session_state.gen_results is not None:
            res = st.session_state.gen_results

            msg_bar.success('Success!', icon='✅')
            output_list = output_results.container()
            for i, gen in enumerate(res):
                gen_box = output_list.expander(f'Generated Code #{i+1}', expanded=True)
                gen_box.code(gen, language='python')
