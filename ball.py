import math
from copy import deepcopy
from point import Point
import numpy as np

class Ball:
    field_size = Point(800, 600)  # Размер поля по умолчанию

    def __init__(self, position, velocity, acceleration, radius):
        self.position = position       # Текущая позиция (Point)
        self.velocity = velocity       # Вектор скорости (Point)
        self.acceleration = acceleration  # Вектор ускорения (Point)
        self.radius = radius           # Радиус мяча
        self.lock = [False, False]
        self.lockedAcceleration = Point(0, 0)

        if velocity.x < 1e-3:
            if (acceleration.x < 0 and position.x < radius + 1e-3) or \
                (acceleration.x > 0 and Ball.field_size.x - position.x < radius + 1e-3):
                self.lock[0] = True
                self.lockedAcceleration.x = self.acceleration.x
                self.acceleration.x = 0
                self.velocity.x = 0
        if velocity.x < 1e-3:
            if (acceleration.y < 0 and position.y < radius + 1e-3) or \
                (acceleration.y > 0 and Ball.field_size.y - position.y < radius + 1e-3):
                self.lock[1] = True
                self.lockedAcceleration.y = self.acceleration.y
                self.acceleration.y = 0
                self.velocity.y = 0

    def get_wall_collision(self):
        """
        Возвращает минимальное время до столкновения с любым из краев поля.
        """
        left, right, up, down = -1, -1, -1, -1

        A = self.acceleration.x / 2
        B = self.velocity.x
        C = self.position.x - self.radius # x0 - x(t)

        if (B ** 2 - 4 * A * C >= 0):
            roots = np.roots([A, B, C])
            buffer = -1
            for i in roots:
                if i > 0:
                    if buffer == -1:
                        buffer = i
                    elif buffer > i:
                        buffer = i
            left = buffer

        C = self.position.x - (self.field_size.x - self.radius) # x0 - x(t)

        if (B ** 2 - 4 * A * C >= 0):
            roots = np.roots([A, B, C])
            buffer = -1
            for i in roots:
                if i > 0:
                    if buffer == -1:
                        buffer = i
                    elif buffer > i:
                        buffer = i
            right = buffer

        A = self.acceleration.y / 2
        B = self.velocity.y
        C = self.position.y - self.radius  # x0 - x(t)

        if (B ** 2 - 4 * A * C >= 0):
            roots = np.roots([A, B, C])
            buffer = -1
            for i in roots:
                if i > 0:
                    if buffer == -1:
                        buffer = i
                    elif buffer > i:
                        buffer = i
            down = buffer

        C = self.position.y - (self.field_size.y - self.radius) # x0 - x(t)

        if (B ** 2 - 4 * A * C >= 0):
            roots = np.roots([A, B, C])
            buffer = -1
            for i in roots:
                if i > 0:
                    if buffer == -1:
                        buffer = i
                    elif buffer > i:
                        buffer = i
            up = buffer



        if right != -1 and (right < left or left == -1) and (right < up or up == -1) and (right < down or down == -1):
            return right, "right"
        elif left != -1 and (left < up or up == -1) and (left < down or down == -1):
            return left, "left"
        elif up != -1 and (up < down or down == -1):
            return up, "up"
        elif down != -1:
            return down, "down"
        return None, None

    def unlockX(self):
        if self.lock[0]:
            self.acceleration.x = self.lockedAcceleration.x
            self.lock[0] = False

    def unlockY(self):
        if self.lock[1]:
            self.acceleration.y = self.lockedAcceleration.y
            self.lock[1] = False

    @staticmethod
    def process_collision(ball1, ball2):
        """
        Перемещает мячи до момента столкновения и меняет их импульсы.
        t — время до столкновения.
        """
        # Сохраняем начальные значения
        p1_start = deepcopy(ball1.position)
        p2_start = deepcopy(ball2.position)

        # Вычисляем нормаль столкновения
        normal = (ball2.position - ball1.position).normalize()

        # Массы (пропорциональны радиусу)
        m1 = ball1.radius ** 2
        m2 = ball2.radius ** 2

        # Относительная скорость
        rel_velocity = ball2.velocity - ball1.velocity

        # Проекция относительной скорости на нормаль
        speed_along_normal = rel_velocity.dot(normal)

        # Если движутся в разные стороны — ничего не делаем
        if speed_along_normal > 0:
            # Возвращаем мячи обратно
            ball1.position = p1_start
            ball2.position = p2_start
            return

        # Коэффициент восстановления (упругий удар)
        e = 1.0  # идеально упругий удар

        # Изменение импульса
        j = -(1 + e) * speed_along_normal / (1/m1 + 1/m2)
        impulse = normal * j

        if abs(impulse.x) > 1e-3:
            ball1.unlockX()
            ball2.unlockX()
        if abs(impulse.y) > 1e-3:
            ball1.unlockY()
            ball2.unlockY()

        # Обновляем скорости
        ball1.velocity = ball1.velocity - impulse / m1
        ball2.velocity = ball2.velocity + impulse / m2

    def update(self, dt):
        """Обновляет позицию мяча на dt секунд"""
        self.position = self.position + self.velocity * dt + self.acceleration * dt ** 2 / 2
        self.velocity = self.velocity + self.acceleration * dt

    def reflect_on_wall(self, side):
        """Отражает мяч от указанной стены (left, right, top, bottom)"""
        if side in ['left', 'right']:
            self.velocity.x *= -1
            if abs(self.velocity.x) < 1e-3:
                self.velocity.x = 0
            if side == 'left':
                self.position.x = self.radius + 1e-8
            if side == 'right':
                self.position.x = Ball.field_size.x - (self.radius + 1e-8)
        elif side in ['up', 'down']:
            if abs(self.velocity.y) < 1e-3:
                self.velocity.y = 0
            self.velocity.y *= -1
            if side == 'down':
                self.position.y = self.radius + 1e-8
            if side == 'up':
                self.position.y = Ball.field_size.y - (self.radius + 1e-8)
