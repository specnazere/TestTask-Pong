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
        pygame.display.set_caption("TestTask-Pong")
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
            self.check_collisions(self.balls[i])

        self.collisions.sort(key=lambda x: x[0])  # Сортируем по времени

    def check_collisions(self, ball):
        t, wall = ball.get_wall_collision()
        if t is not None:
            self.collisions.append((t, 'wall', ball, wall))
        nearestTime = None
        nearestBall = None
        for i in range(0, len(self.balls)):
            if self.balls[i] == ball: continue
            t = Ball.get_collision(ball, self.balls[i])
            if t is not None:
                if nearestTime is None or t < nearestTime:
                    nearestTime = t
                    nearestBall = self.balls[i]
        if nearestBall is not None:
            self.collisions.append((nearestTime, 'ball', ball, nearestBall))

    def reprocess_collisions(self, ball):
        colIndex = 0
        while colIndex < len(self.collisions):
            if self.collisions[colIndex][2] == ball or self.collisions[colIndex][3] == ball:
                self.collisions.pop(colIndex)
            else:
                colIndex += 1
        self.check_collisions(ball)

    def update_balls(self, dt):
        """Обновляет позиции и обрабатывает столкновения"""

        # Если нет ни одного столкновения, просто делаем обычный update
        if not self.collisions:
            for ball in self.balls:
                ball.update(dt)
            return

        for ball1 in self.balls:
            for ball2 in self.balls:
                if ball1 != ball2:
                    if (ball1.position - ball2.position).norm_sq() < (ball1.radius + ball2.radius) ** 2:
                        Ball.process_collision(ball1, ball2)
                        self.reprocess_collisions(ball1)
                        self.reprocess_collisions(ball2)

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
                self.reprocess_collisions(obj1)
                self.reprocess_collisions(obj2)
            elif collision_type == 'wall':
                obj1.reflect_on_wall(obj2)
                self.reprocess_collisions(obj1)

            # После обработки столкновения, обновляем всё остальное
            remaining_time = dt - nearest_t

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