from code_translator import *
import streamlit as st


if __name__ == '__main__':
    test_container = st.container()

    test_container.header('⚙️ Test Code Generation')

    if 'test_input' not in st.session_state:
        st.session_state.test_input = None
    if 'test_results' not in st.session_state:
        st.session_state.test_results = None

    test_manual = test_container.expander('See Example For Help')
    test_manual.write('')

    msg_bar = test_container.empty()
    test_ui = test_container.container()
    input_cols, output_cols = test_ui.columns(2, gap='medium')

    test_input_form = input_cols.form(key='testcode_input')
    with test_input_form:
        test_input = test_input_form.text_area('Enter the code', height=500, key='test_input_code')
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
