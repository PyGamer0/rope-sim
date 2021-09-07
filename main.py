from pyglet.math import Vec2
import pyglet

GRAVITY = Vec2(0, -9.8)


class Point:
    def __init__(self, position, batch, is_locked=False):
        self.position = position
        self.is_locked = is_locked

        self._previous_position = position

        self.shape = pyglet.shapes.Circle(position.x, position.y, 10, color=(230, 230, 240), batch=batch)

    def update(self, dt):
        if self.is_locked:
            return

        position_before_update = self.position
        self.position = self.position + (self.position - self._previous_position)
        self.position = self.position + (GRAVITY.scale(dt ** 2))
        self._previous_position = position_before_update

        self.shape.position = self.position

    def update_color(self):
        if self.is_locked:
            self.shape.color = (230, 100, 100)
            return
        self.shape.color = (230, 230, 240)

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

    def find_point(self, x, y):
        # Checks if the x,y coords are on a point.
        # Returns -1 if point not found
        i = 0
        while i < len(self.points) - 1:
            p = self.points[i]
            i += 1

            d = p.position.distance(Vec2(x, y))
            if d <= 10.0:
                return i - 1
        return -1

    def find_stick(self, p):
        # Given a point find the index of the stick
        # that is connected to it
        # Returns -1 if not found
        i = 0
        while i < len(self.sticks) - 1:
            s = self.sticks[i]
            i += 1

            if (s.pos_a == p) or (s.pos_b == p):
                return i - 1
        return -1

    def update(self, dt):
        for point in self.points:
            point.update_color()

        if self.paused:
            return

        for point in self.points:
            point.update(dt)

        for _ in range(5):
            for stick in self.sticks:
                stick.update(dt)

    def on_draw(self):
        self.clear()
        self.batch.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        point_i = self.find_point(x, y)
        if button == pyglet.window.mouse.LEFT:
            if point_i == -1:
                self.points.append(Point(Vec2(x, y), self.batch))
            else:
                self.points[point_i].is_locked = not self.points[point_i].is_locked
        else:
            if point_i == -1:
                return
            stick_i = self.find_stick(self.points[point_i])
            if stick_i != -1:
                self.sticks[stick_i].line.delete()
                self.sticks.pop(stick_i)
            self.points[point_i].shape.delete()
            self.points.pop(point_i)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.paused = not self.paused


win = Window(800, 800)

pyglet.clock.schedule_interval(win.update, 1 / 60)
pyglet.app.run()
