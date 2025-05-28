if __name__ == "__main__":
    from point import Point
    from scene import Scene
    from ball import Ball
    from random import randint
    from fileParser import FileParser

    width = 1000
    height = 1000

    scene = Scene(width, height)

    for i in range(10):
       for j in range(10):
           scene.add_ball(Ball(Point(width / 11 * (i + 1), height / 11 * (j + 1)), Point(randint(-50, 50), randint(-50, 50)), Point(randint(-50, 50), randint(-50, 50)), 20))

    scene.run()