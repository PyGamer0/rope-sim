from pyglet.math import Vec2
import pyglet

GRAVITY = Vec2(0, -9.8)

class Point:
    def __init__(self, position, is_locked=False):
        self.position = position
        self.is_locked = is_locked

        self._previous_position = position
    
    def update(self, dt):
        if self.is_locked:
            return

        position_before_update = self.position
        self.position = self.position + (self.position - self._previous_position)
        self.position = self.position + (GRAVITY.scale(dt ** 2))
        self._previous_position = position_before_update
    
    def draw(self):
        shape = pyglet.shapes.Circle(self.position.x, self.position.y, 5)
        shape.color = (230, 230, 240)
        shape.draw()

class Stick:
    def __init__(self, pos_a, pos_b, length=None):
        self.pos_a = pos_a
        self.pos_b = pos_b

        if length is not None:
            self.length = length
        else:
            self.length = self.pos_a.position.distance(self.pos_b.position)

    def update(self, dt):
        center = (self.pos_a.position + self.pos_b.position).scale(0.5)
        direction = (self.pos_a.position - self.pos_b.position).normalize()

        if not self.pos_a.is_locked:
            self.pos_a.position = center + direction.scale(self.length / 2)

        if not self.pos_b.is_locked:
            self.pos_b.position = center - direction.scale(self.length / 2)

    def draw(self):
        shape = pyglet.shapes.Line(self.pos_a.position.x, self.pos_a.position.y,
                self.pos_b.position.x, self.pos_b.position.y)
        shape.color = (230, 230, 240)
        shape.draw()

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.points = [Point(Vec2(100, 400)),
                Point(Vec2(150, 400)),
                Point(Vec2(200, 400)),
                Point(Vec2(250, 400)),
                Point(Vec2(350, 400)),
                Point(Vec2(400, 400), True)]
        self.sticks = [Stick(self.points[0], self.points[1]),
                Stick(self.points[1], self.points[2]),
                Stick(self.points[2], self.points[3]),
                Stick(self.points[3], self.points[4]),
                Stick(self.points[4], self.points[5]),
                ]
        self.paused = False

    def update(self, dt):
        if self.paused:
            return

        for point in self.points:
            point.update(dt)

        for i in range(5):
            for stick in self.sticks:
                stick.update(dt)

    def on_draw(self):
        self.clear()

        for stick in self.sticks:
            stick.draw()

        for point in self.points:
            point.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        self.points.append(Point(Vec2(x, y)))

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.paused = not self.paused

win = Window(800, 800)

pyglet.clock.schedule_interval(win.update, 1 / 60)
pyglet.app.run()

