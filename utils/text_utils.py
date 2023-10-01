def split_sections(input: str, delimiter: str):
    sections = input.split(delimiter)
    sections = map(lambda s: s.strip(), sections)

    return sections


if __name__ == '__main__':
    input = """
Peace brothers and sisters
---
弟兄姊妹们平安
"""
    print(split_sections(input, "---\n"))
