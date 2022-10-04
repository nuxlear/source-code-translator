import os
from pathlib import Path
import uuid


tmp_input_dir = Path('tmp_input')


def save_code_to_tmp_file(code):
    os.makedirs(tmp_input_dir, exist_ok=True)
    filename = f'{uuid.uuid4()}.py'
    file_path = tmp_input_dir / filename

    with open(file_path, 'w') as f:
        f.write(code)

    return file_path
