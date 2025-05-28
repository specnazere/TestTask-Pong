if __name__ == "__main__":
    from point import Point
    from scene import Scene
    from ball import Ball
    from random import randint

    width = 1000
    height = 1000

    scene = Scene(width, height)

    b1 = Ball(Point(200, 100), Point(0, 0), Point(0, 0), 20)
    b2 = Ball(Point(200, 200), Point(90, 20), Point(0, -10), 20)
    b3 = Ball(Point(100, 100), Point(100, 0), Point(0, 0), 20)

    scene.add_ball(b1)
    scene.add_ball(b2)
    scene.add_ball(b3)

    #for i in range(8):
    #    for j in range(8):
    #        scene.add_ball(Ball(Point(width / 11 * (i + 1), height / 11 * (j + 1)), Point(randint(-50, 50), randint(-50, 50)), Point(randint(-50, 50), randint(-50, 50)), 20))


    scene.run()