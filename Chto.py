import yaml
import argparse
import re
import sys

class ConfigTranslator:
    def __init__(self):
        self.constants = {}

    def translate(self, data):
        """Преобразует YAML-данные в УКЯ."""
        if isinstance(data, dict):
            return "\n".join(f"var {key} {self.translate(value)}" for key, value in data.items())
        elif isinstance(data, list):
            return f"({{ {', '.join(self.translate(value) for value in data)} }})"
        elif isinstance(data, str):
            return f"[[{data}]]"
        elif isinstance(data, (int, float)):
            return str(data)
        else:
            raise ValueError(f"Unsupported data type: {type(data)}")

    def resolve_constants(self, expression):
        """Вычисляет значение константного выражения ?(имя)."""
        match = re.fullmatch(r"\?\((\w+)\)", expression)
        if match:
            name = match.group(1)
            if name not in self.constants:
                raise ValueError(f"Undefined constant: {name}")
            return self.constants[name]
        return expression

    def process_file(self, input_file):
        """Читает YAML-файл и преобразует его в УКЯ."""
        try:
            with open(input_file, "r") as f:
                data = yaml.safe_load(f)
                return self.translate(data)
        except yaml.YAMLError as e:
            raise SyntaxError(f"Error parsing YAML: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {input_file}")

def main():
    parser = argparse.ArgumentParser(description="YAML to УКЯ Translator")
    parser.add_argument("--input", required=True, help="Path to the input YAML file")
    args = parser.parse_args()

    translator = ConfigTranslator()

    try:
        output = translator.process_file(args.input)
        print(output)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
