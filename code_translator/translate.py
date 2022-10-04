from code_translator.core import generate_explanation
from code_translator.validate import find_vulnerabilities, make_prompt_query_for_enhancement, is_same_vulnerability
from code_translator.utils import save_code_to_tmp_file

import os


def get_explanation(code, n=3):
    query = '"""\nThe explanation of the Python 3 code above is here:\n1. '
    prompt = f'{code}\n\n{query}'

    candidates = generate_explanation(prompt, num_results=n, max_tokens=384)

    cand_texts = [x.text.split('"""')[0] for x in candidates if x.finish_reason == 'stop']
    res_texts = [x for x in cand_texts if len(x.strip()) > 0]
    return [f'{query}{x}"""' for x in res_texts]


def get_enhancements(code, n=3):
    file_path = save_code_to_tmp_file(code)

    vulnerabilities = find_vulnerabilities(str(file_path))
    results = []
    for v in vulnerabilities:
        prompt = make_prompt_query_for_enhancement(v, code)

        candidates = generate_explanation(prompt, num_results=n, max_tokens=384)
        cand_texts = [x.text for x in candidates if x.finish_reason == 'stop']
        cand_texts = list(set(cand_texts))

        answers = []
        for cand_text in cand_texts:
            cand_file_path = save_code_to_tmp_file(cand_text)

            fixed_vuls = find_vulnerabilities(str(cand_file_path))

            is_valid_code = all([fv['type'] not in ['error', 'fatal'] for fv in fixed_vuls])
            is_vul_remains = any([is_same_vulnerability(v, fv) for fv in fixed_vuls])
            if is_valid_code and not is_vul_remains:
                answers.append(cand_text)

            os.remove(cand_file_path)

        results.append((v, answers))

    os.remove(file_path)
    return results


def get_modification(code, query, n=3):
    pass


if __name__ == '__main__':
    pass
