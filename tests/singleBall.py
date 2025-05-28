if __name__ == "__main__":
    from point import Point
    from scene import Scene
    from ball import Ball
    from random import randint
    from fileParser import FileParser

    width = 200
    height = 200

    scene = Scene(width, height)

    b1 = Ball(Point(100, 100), Point(0, 0), Point(0, 0), 20)
    scene.add_ball(b1)

    scene.run()