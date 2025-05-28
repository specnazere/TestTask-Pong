from threading import Timer

import pygame
import sys

from ball import Ball  # Предполагается, что Ball уже определён
from point import Point  # Также должен быть определён
from tickManager import TickManager

class Scene:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.collisions = []
        self.balls = []

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Physics Balls Simulation")
        self.clock = pygame.time.Clock()
        self.running = True

        # Установка размера поля для всех мячей
        Ball.field_size = Point(width, height)

    def add_ball(self, ball):
        """Добавляет мяч в сцену"""
        self.balls.append(ball)

    def handle_events(self):
        """Обрабатывает события из Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def post_init(self):
        # Проверяем все пары мячей на столкновение
        for i in range(len(self.balls)):
            nearestTime = None
            nearestBall = None
            for j in range(i + 1, len(self.balls)):
                t = Ball.get_collision(self.balls[i], self.balls[j])
                if t is not None:
                    if nearestTime is None or t < nearestTime:
                        nearestTime = t
                        nearestBall = self.balls[j]
            if nearestBall is not None:
                self.collisions.append((nearestTime, 'ball', self.balls[i], nearestBall))

        # Проверяем столкновения с границами
        for ball in self.balls:
            t, wall = ball.get_wall_collision()
            if t is not None:
                self.collisions.append((t, 'wall', ball, wall))

        self.collisions.sort(key=lambda x: x[0])  # Сортируем по времени

    def update_balls(self, dt):
        """Обновляет позиции и обрабатывает столкновения"""

        # Если нет ни одного столкновения, просто делаем обычный update
        if not self.collisions:
            for ball in self.balls:
                ball.update(dt)
            return

        # Находим ближайшее столкновение
        nearest_t, collision_type, obj1, obj2 = self.collisions[0]
        if nearest_t >= dt:
            self.collisions = [(x[0] - dt, x[1], x[2], x[3]) for x in self.collisions]
            for ball in self.balls:
                ball.update(dt)
        else:
            # Обновляем всё до этого момента
            for ball in self.balls:
                ball.update(nearest_t)

            # Обрабатываем само столкновение
            if collision_type == 'ball':
                Ball.process_collision(obj1, obj2)  # t=0, потому что уже переместили
                colIndex = 0
                while colIndex < len(self.collisions):
                    if self.collisions[colIndex][2] == obj1 or self.collisions[colIndex][2] == obj2 \
                        or self.collisions[colIndex][3] == obj1 or self.collisions[colIndex][3] == obj2:
                        self.collisions.pop(colIndex)
                    else:
                        colIndex += 1
            elif collision_type == 'wall':
                obj1.reflect_on_wall(obj2)

                colIndex = 0
                while colIndex < len(self.collisions):
                    if self.collisions[colIndex][2] == obj1:
                        self.collisions.pop(colIndex)
                    else:
                        colIndex += 1

            # После обработки столкновения, обновляем всё остальное
            remaining_time = dt - nearest_t

            # Проверяем все пары мячей на столкновение
            nearestTime = None
            nearestBall = None
            for i in range(0, len(self.balls)):
                if self.balls[i] == obj1: continue
                t = Ball.get_collision(obj1, self.balls[i])
                if t is not None:
                    if nearestTime is None or t < nearestTime:
                        nearestTime = t
                        nearestBall = self.balls[i]
            if nearestBall is not None:
                self.collisions.append((nearestTime, 'ball', obj1, nearestBall))

            t, wall = obj1.get_wall_collision()
            if t is not None:
                self.collisions.append((t, 'wall', obj1, wall))
            if collision_type == 'ball':
                t, wall = obj2.get_wall_collision()
                if t is not None:
                    self.collisions.append((t, 'wall', obj2, wall))
                nearestTime = None
                nearestBall = None
                for i in range(0, len(self.balls)):
                    if self.balls[i] == obj2: continue
                    t = Ball.get_collision(obj2, self.balls[i])
                    if t is not None:
                        if nearestTime is None or t < nearestTime:
                            nearestTime = t
                            nearestBall = self.balls[i]
                if nearestBall is not None:
                    self.collisions.append((nearestTime, 'ball', obj2, nearestBall))

            self.collisions.sort(key=lambda x: x[0])  # Сортируем по времени
            self.collisions = [(x[0] - nearest_t, x[1], x[2], x[3]) for x in self.collisions]
            self.update_balls(remaining_time)

    def draw_balls(self):
        """Отрисовывает все мячи"""
        self.screen.fill((0, 0, 0))  # Чёрный фон
        for ball in self.balls:
            pygame.draw.circle(
                self.screen,
                (255, 255, 255),
                (int(ball.position.x), int(ball.position.y)),
                int(ball.radius)
            )
        pygame.display.flip()

    def run(self, fps=60):
        """Запуск главного цикла"""
        self.post_init()
        TickManager.initialize()
        while self.running:
            self.handle_events()
            self.update_balls(TickManager.get_previous_tick_length())
            self.draw_balls()
            TickManager.tick()

        pygame.quit()
        sys.exit()