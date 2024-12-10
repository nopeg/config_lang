import re
import toml
import sys
import math


def evaluate_expression(expression):
    tokens = expression.split()
    stack = []
    for token in tokens:
        if token.isdigit():
            stack.append(int(token))
        elif token == '+':
            stack.append(stack.pop() + stack.pop())
        elif token == 'ord(':
            if stack:
                if(len(str(stack[-1])) != 1):
                    print("ord() expected a character, but string of other length found")
                    stack.pop()
                else: stack.append(ord(str(stack.pop())))
    return stack[0] if stack else None


def parse_config(text):
    config = {}
    text = re.sub(r'#\|[\s\S]*?\|#', '', text)
    lines = text.splitlines()
    current_dict = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # Словари
        if line == "{":
            current_dict = {}
            continue
        elif line == "}":
            config.update(current_dict)
            current_dict = None
            continue


        if ":= ^(" in line:
            line = line.replace('^', '')

        expr_match = re.match(r'(\w+)\s*:=\s*\((.*?)\);?', line)
        if expr_match:
            name, expression = expr_match.groups()
            result = evaluate_expression(expression)
            if result:
                if current_dict is not None:
                    current_dict[name] = result
                else:
                    config[name] = result
            else:
                print("Error in line {", line, "}")
            continue
        else:
            # Обработка обычных ключ-значений
            kv_match = re.match(r'(\w+)\s*:=\s*(.+?);', line)
            if kv_match:
                name, value = kv_match.groups()
                value = value.strip()

                if value == 'true':
                    value = True
                elif value == 'false':
                    value = False
                # Строки
                elif value.startswith("[[") and value.endswith("]]"):
                    value = value.strip("[[]]")
                elif value.isdigit():
                    value = int(value)

                if current_dict is not None:
                    current_dict[name] = value
                else:
                    config[name] = value
            else:
                print("Error in line {", line, "}")

    return config


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <output_file.yaml>")
        sys.exit(1)

    output_file = sys.argv[1]
    input_text = sys.stdin.read()

    config = parse_config(input_text)

    with open(output_file, 'w') as f:
        toml.dump(config, f)
