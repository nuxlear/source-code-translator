from pylint.lint import PyLinter, Run
from pylint.reporters.text import TextReporter
from pylint.reporters import JSONReporter
from io import StringIO
# from flake8.api import legacy as flake8
from contextlib import redirect_stdout
import json
import os

from code_translator.utils import save_code_to_tmp_file


def find_vulnerabilities(code):
    code_file = save_code_to_tmp_file(code)

    lint_output = StringIO()
    reporter = JSONReporter(lint_output)

    with redirect_stdout(lint_output):
        Run([str(code_file), '--output-format=json', '--disable=E0602,E1101,E0401,W1401'], reporter=reporter, exit=False)

    report = lint_output.getvalue()
    report = json.loads(report)

    os.remove(code_file)

    vulnerabilities = [x for x in report if x['type'] in ['warning', 'error', 'fatal']]
    return vulnerabilities


def make_prompt_query_for_enhancement(v, code):
    text = f'#### Fix the problem "{v["message"]}" on line {v["line"]} of the code below\n\n' \
           f'## Code with problem:\n{code}\n\n' \
           f'## Fixed version:\n'
    return text


def is_same_vulnerability(v1, v2):
    keys = ['type', 'module', 'obj', 'line', 'message-id']
    return all([v1.get(k) == v2.get(k) for k in keys])


if __name__ == '__main__':
    pass
