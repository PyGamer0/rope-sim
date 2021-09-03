from pyglet.math import Vec2
import pyglet

GRAVITY = Vec2(0, -9.8)


class Point:
    def __init__(self, position, batch, is_locked=False):
        self.position = position
        self.is_locked = is_locked

        self._previous_position = position

        self.shape = pyglet.shapes.Circle(position.x, position.y, 5, color=(230, 230, 240), batch=batch)

    def update(self, dt):
        if self.is_locked:
            return

        position_before_update = self.position
        self.position = self.position + (self.position - self._previous_position)
        self.position = self.position + (GRAVITY.scale(dt ** 2))
        self._previous_position = position_before_update
        self.shape.position = self.position


class Stick:
    def __init__(self, pos_a, pos_b, batch, length=None):
        self.pos_a = pos_a
        self.pos_b = pos_b

        self.line = pyglet.shapes.Line(self.pos_a.position.x, self.pos_a.position.y,
                                       self.pos_b.position.x, self.pos_b.position.y,
                                       color=(230, 230, 240), batch=batch)

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

        self.line.position = *self.pos_a.position, *self.pos_b.position


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.batch = pyglet.graphics.Batch()

        self.points = [Point(Vec2(100, 400), self.batch),
                       Point(Vec2(150, 400), self.batch),
                       Point(Vec2(200, 400), self.batch),
                       Point(Vec2(250, 400), self.batch),
                       Point(Vec2(350, 400), self.batch),
                       Point(Vec2(400, 400), self.batch, True)]
        self.sticks = [Stick(self.points[0], self.points[1], self.batch),
                       Stick(self.points[1], self.points[2], self.batch),
                       Stick(self.points[2], self.points[3], self.batch),
                       Stick(self.points[3], self.points[4], self.batch),
                       Stick(self.points[4], self.points[5], self.batch),
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
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.points.append(Point(Vec2(x, y), self.batch))

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.paused = not self.paused


win = Window(800, 800)

pyglet.clock.schedule_interval(win.update, 1 / 60)
pyglet.app.run()
