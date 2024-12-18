import yaml
import sys

# Словарь для замены цифр на слова
DIGIT_TO_WORD = {
    "0": "ZERO",
    "1": "ONE",
    "2": "TWO",
    "3": "THREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINE"
}

# Глобальные переменные для управления многострочными комментариями
aaa = []
t = 0

def fix_name(name):
    """
    Исправляет имя, если оно не соответствует формату [A-Z]+.
    """
    fixed_name = ""
    for char in name:
        if char.islower():
            fixed_name += char.upper()
        elif char.isdigit():
            fixed_name += DIGIT_TO_WORD.get(char, "")
        elif char.isupper():
            fixed_name += char
        else:
            raise ValueError(f"Недопустимый символ в имени: {char}")
    return fixed_name

def process_value(value):
    """
    Обрабатывает значение и возвращает его в выходном формате.
    """
    global t, aaa

    if isinstance(value, dict):
        return process_dict(value)
    elif isinstance(value, list):
        return process_list(value)
    elif isinstance(value, str):
        if value.startswith("?"):  # Переводим в формат ?(имя)
            return f"?({value[1:]})"
        if value.startswith("#"):  # Обрабатываем комментарий
            if t == 0:
                aaa = ["=begin"]
                t = 1
            aaa.append(value[1:])  # Добавляем строку комментария без символа #
            return None  # Возвращаем None, чтобы не добавлять это значение в вывод
        return f"[[{value}]]"
    elif isinstance(value, (int, float)):
        output = []
        if t == 1:
            t = 0
            aaa.append("=end")
            for line in aaa:
                output.append(line)
            aaa = []
            output.append(str(value))
        return "\n".join(output)
    else:
        raise ValueError(f"Неподдерживаемый тип значения: {type(value)}")

def process_dict(d):
    """
    Обрабатывает словарь и возвращает его в выходном формате.
    """
    global t, aaa

    output = []
    if t == 1:
        t = 0
        aaa.append("=end")
        for line in aaa:
            output.append(line)
        aaa = []
    for key, value in d.items():
        fixed_key = fix_name(key)
        if isinstance(value, dict):
            output.append(f"var {fixed_key} {{\n{process_dict(value)}\n}}")
        elif isinstance(value, list):
            output.append(f"var {fixed_key} {process_list(value)}")
        else:
            processed_value = process_value(value)
            if processed_value is not None:  # Проверяем, что значение не является комментарием
                output.append(f"var {fixed_key} {processed_value}")
    return "\n".join(output)

def process_list(lst):
    """
    Обрабатывает список и возвращает его в выходном формате.
    """
    global t, aaa

    output = []
    if t == 1:
        t = 0
        aaa.append("=end")
        for line in aaa:
            output.append(line)
        aaa = []
    for item in lst:
        if isinstance(item, dict):
            if len(item) == 1:  # Один ключ в словаре
                key, value = next(iter(item.items()))
                fixed_key = fix_name(key)
                if value is None:  # Ключ без значения
                    output.append(f"{fixed_key}")
                else:  # Ключ со значением
                    processed_value = process_value(value)
                    if processed_value is not None:  # Проверяем, что значение не является комментарием
                        output.append(f"{fixed_key}: {processed_value}")
            else:
                raise ValueError(f"Словарь в списке содержит более одного ключа: {item}")
        elif isinstance(item, str):  # Ключ без значения
            fixed_key = fix_name(item)
            output.append(f"{fixed_key}")
        else:
            processed_value = process_value(item)
            if processed_value is not None:  # Проверяем, что значение не является комментарием
                output.append(processed_value)
    return f"<[ {', '.join(output)} ]>"

def process_yaml_string(yaml_string):
    """
    Обрабатывает строку YAML и возвращает результат в формате УКЯ.
    """
    global t, aaa

    # Парсим YAML-строку
    data = yaml.safe_load(yaml_string)
    # Генерируем вывод
    return process_value(data)

def main():
    """
    Основная функция CLI.
    """
    global t, aaa

    if len(sys.argv) != 2:
        print("Использование: python config_converter.py <путь_к_файлу.yaml>")
        sys.exit(1)
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        content = file.read()
    try:
        output = process_yaml_string(content)
        print(output)
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
