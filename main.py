import gradio as gr
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# response = openai.Completion.create(
#   model="code-davinci-002",
#   prompt="# Python 3 \ndef remove_common_prefix(x, prefix, ws_prefix): \n    x[\"completion\"] = x[\"completion\"].str[len(prefix) :] \n    if ws_prefix: \n        # keep the single whitespace as prefix \n        x[\"completion\"] = \" \" + x[\"completion\"] \nreturn x \n\n# Explanation of what the code does\n\n#",
#   temperature=0,
#   max_tokens=64,
#   top_p=1.0,
#   frequency_penalty=0.0,
#   presence_penalty=0.0
# )


def generate_explanation(input_text, mode=None):
    if mode == 'generate':
        input_text = f'"""\n{input_text}\n"""'
    if mode == 'explain':
        input_text = f'{input_text}\n\n"""\nHere\'s what the above Python 3 code is doing:\n1. '
    if mode == 'test':
        input_text = f'{input_text}\n\n# Test the code above\n\n'

    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=input_text,
        temperature=0.5,
        max_tokens=384,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.05
    )
    answer = response.choices[0]
    return answer.text


if __name__ == '__main__':
#     code = '''name = input("What is your name? ")
# print("Hello, " + name)'''
#     generate_explanation(code)
    demo = gr.Interface(
        fn=generate_explanation,
        inputs=[
            gr.Textbox(lines=40, max_lines=40),
            gr.Radio(choices=['generate', 'explain', 'test'],
                     label=['Generate Code', 'Explain Code', 'Test Code']),
        ],
        outputs=[
            gr.Textbox(lines=50, max_lines=50),
        ]
    )
    demo.launch()
