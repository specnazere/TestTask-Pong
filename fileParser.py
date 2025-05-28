from ball import Ball
from point import Point

import re
import random

class FileParser:
    @staticmethod
    def parse_balls_from_file(filename):
        objects = []
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    raise ValueError(f"[Строка {line_num}] Недостаточно данных: '{line}'")

                obj_type, rest = parts[0], parts[1]

                if obj_type != "Ball":
                    raise ValueError(f"[Строка {line_num}] Неизвестный тип объекта: '{obj_type}'")

                tokens = rest.split()

                processed_tokens = []
                for token in tokens:
                    if token.lower().startswith("rand(") and token.endswith(")"):
                        try:
                            content = token[4:-1].strip()
                            min_val, max_val = map(float, content.split(','))
                            random_val = random.uniform(min_val, max_val)
                            processed_tokens.append(str(random_val))
                        except Exception as e:
                            raise ValueError(
                                f"[Строка {line_num}] Ошибка в rand(): '{token}': {e}"
                            )
                    else:
                        try:
                            processed_tokens.append(float(token))
                        except ValueError:
                            raise ValueError(
                                f"[Строка {line_num}] Неверное значение: '{token}'. "
                                "Ожидалось число или функция."
                            )

                if len(processed_tokens) != 7:
                    raise ValueError(
                        f"[Строка {line_num}] Неверное количество параметров для Ball: "
                        f"получено {len(processed_tokens)}, ожидается 7"
                    )

                data = list(map(float, processed_tokens))

                pos = Point(data[0], data[1])
                vel = Point(data[2], data[3])
                acc = Point(data[4], data[5])
                radius = data[6]

                ball = Ball(pos, vel, acc, radius)
                objects.append(ball)

        return objects