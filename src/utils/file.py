def read_text_file(file_name: str) -> str:
    with open(file_name, encoding="utf-8") as f:
        return f.read()


def create_text_file(file_name: str, text: str = "") -> int:
    with open(file_name, "w", encoding="utf-8") as f:
        return f.write(text)
