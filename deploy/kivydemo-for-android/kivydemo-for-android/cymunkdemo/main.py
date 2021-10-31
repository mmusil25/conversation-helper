import cymunk as cy
from os.path import dirname, join
from kivy.clock import Clock
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import DictProperty, ListProperty
from kivy.core.image import Image
from random import random
from kivy.lang import Builder

Builder.load_string('''
<Playground>:
    Label:
        text: 'circles: %d' % len(root.blist)
''')

class Playground(Widget):

    cbounds = ListProperty([])
    cmap = DictProperty({})
    blist = ListProperty([])

    def __init__(self, **kwargs):
        self._hue = 0
        super(Playground, self).__init__(**kwargs)
        self.init_physics()
        self.bind(size=self.update_bounds, pos=self.update_bounds)
        self.texture = Image(join(dirname(__file__), 'circle.png'), mipmap=True).texture
        Clock.schedule_interval(self.step, 1 / 30.)

    def init_physics(self):
        # create the space for physics simulation
        self.space = space = cy.Space()
        space.iterations = 30
        space.gravity = (0, -700)
        space.sleep_time_threshold = 0.5
        space.collision_slop = 0.5

        # create 4 segments that will act as a bounds
        for x in xrange(4):
            seg = cy.Segment(space.static_body,
                    cy.Vec2d(0, 0), cy.Vec2d(0, 0), 0)
            seg.elasticity = 0.6
            #seg.friction = 1.0
            self.cbounds.append(seg)
            space.add_static(seg)

        # update bounds with good positions
        self.update_bounds()

    def update_bounds(self, *largs):
        assert(len(self.cbounds) == 4)
        a, b, c, d = self.cbounds
        x0, y0 = self.pos
        x1 = self.right
        y1 = self.top

        self.space.remove_static(a)
        self.space.remove_static(b)
        self.space.remove_static(c)
        self.space.remove_static(d)
        a.a = (x0, y0)
        a.b = (x1, y0)
        b.a = (x1, y0)
        b.b = (x1, y1)
        c.a = (x1, y1)
        c.b = (x0, y1)
        d.a = (x0, y1)
        d.b = (x0, y0)
        self.space.add_static(a)
        self.space.add_static(b)
        self.space.add_static(c)
        self.space.add_static(d)

    def step(self, dt):
        self.space.step(1 / 30.)
        self.update_objects()

    def update_objects(self):
        for body, obj in self.cmap.iteritems():
            p = body.position
            radius, color, rect = obj
            rect.pos = p.x - radius, p.y - radius
            rect.size = radius * 2, radius * 2

    def add_random_circle(self):
        self.add_circle(
            self.x + random() * self.width,
            self.y + random() * self.height,
            10 + random() * 50)

    def add_circle(self, x, y, radius):
        # create a falling circle
        body = cy.Body(100, 1e9)
        body.position = x, y
        circle = cy.Circle(body, radius)
        circle.elasticity = 0.6
        #circle.friction = 1.0
        self.space.add(body, circle)

        with self.canvas.before:
            self._hue = (self._hue + 0.01) % 1
            color = Color(self._hue, 1, 1, mode='hsv')
            rect = Rectangle(
                texture=self.texture,
                pos=(self.x - radius, self.y - radius),
                size=(radius * 2, radius * 2))
        self.cmap[body] = (radius, color, rect)

        # remove the oldest one
        self.blist.append((body, circle))
        if len(self.blist) > 200:
            body, circle = self.blist.pop(0)
            self.space.remove(body)
            self.space.remove(circle)
            radius, color, rect = self.cmap.pop(body)
            self.canvas.before.remove(color)
            self.canvas.before.remove(rect)

    def on_touch_down(self, touch):
        self.add_circle(touch.x, touch.y, 10 + random() * 20)

    def on_touch_move(self, touch):
        self.add_circle(touch.x, touch.y, 10 + random() * 20)

class PhysicsApp(App):
    def build(self):
        return Playground()

if __name__ == '__main__':
    PhysicsApp().run()
