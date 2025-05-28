import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Можно складывать только точки")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Point):
            raise TypeError("Можно вычитать только точки")
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Можно умножать только на число")
        return Point(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Можно делить только на число")
        if scalar == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        return Point(self.x / scalar, self.y / scalar)

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def norm_sq(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        length = math.sqrt(self.norm_sq())
        if length == 0:
            return Point(0, 0)
        return self / length

    def __rmul__(self, scalar):
        # Позволяет писать: 2 * point
        return self * scalar

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y