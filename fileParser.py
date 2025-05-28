from ball import Ball
from point import Point

import re
import random

class FileParser:
    @staticmethod
    def parse_balls_from_file(filename):
        objects = []
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                parts = line.split(maxsplit=1)
                if len(parts) < 2:
                    raise ValueError(f"Недостаточно данных в строке: {line}")

                obj_type, rest = parts[0], parts[1]

                if obj_type != "Ball":
                    raise ValueError(f"Неизвестный тип объекта: {obj_type}")

                tokens = rest.split()

                processed_tokens = []
                for token in tokens:
                    if token.startswith("rand(") and token.endswith(")"):
                        match = re.match(r'rand\(([-+]?\d*\.?\d+)\.\.([-+]?\d*\.?\d+)\)', token)
                        if match:
                            min_val = float(match.group(1))
                            max_val = float(match.group(2))
                            random_val = random.uniform(min_val, max_val)
                            processed_tokens.append(str(random_val))
                        else:
                            raise ValueError(f"Неверный формат случайного значения: {token}")
                    else:
                        processed_tokens.append(token)

                if len(processed_tokens) != 7:
                    raise ValueError(f"Неверное количество параметров для Ball: {line}")

                data = list(map(float, processed_tokens))

                pos = Point(data[0], data[1])
                vel = Point(data[2], data[3])
                acc = Point(data[4], data[5])
                radius = data[6]

                ball = Ball(pos, vel, acc, radius)
                objects.append(ball)

        return objects