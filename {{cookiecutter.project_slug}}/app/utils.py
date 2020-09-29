import tomlkit

from pathlib import Path


def get_project_info():
    # Ref: https://github.com/rominf/poetry-version
    d = Path(__file__)
    result = None
    while d.parent != d and result is None:
        d = d.parent
        pyproject_toml_path = d / 'pyproject.toml'
        if pyproject_toml_path.exists():
            with open(file=str(pyproject_toml_path)) as f:
                pyproject_toml = tomlkit.parse(string=f.read())
                result = pyproject_toml['tool']['poetry']
    return result
