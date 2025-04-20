from pathlib import Path


def read_prompt_template(appDirRelativePath: str) -> str:
    """Read the prompt template from file."""
    template_path = Path(__file__).resolve().parent.parent / appDirRelativePath
    try:
        return template_path.read_text()
    except FileNotFoundError:
        raise FileNotFoundError("The specified template file was not found.")
