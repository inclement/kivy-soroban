from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import *
from kivy.clock import Clock

class Rod(BoxLayout):
    pass

class BeadSlider(Widget):
    beads = NumericProperty(1)
    snap = BooleanProperty(True)
    positions = NumericProperty(6)
    position_dist = NumericProperty()

    def on_pos(self, *args):
        self.update_beads()
    def on_size(self, *args):
        self.update_beads()
    def on_position_dist(self, *args):
        self.update_beads()

    def update_beads(self):
        self.reset_beads()
        for bead in self.children:
            bead.x = self.x
            bead.width = self.width
            bead.height = self.position_dist

    def on_beads(self, *args):
        self.reset_beads()
            
    def reset_beads(self, *args):
        '''Moves all the beads to a suitable initial position.'''
        #self.update_beads()
        while len(self.children) < self.beads:
            self.add_widget(Bead())
        while len(self.children) > self.beads:
            self.remove_widget(self.children[-1])
        i = 0
        for bead in self.children:
            bead.y = self.y + i*self.position_dist
            print bead, bead.y, self.position_dist
            i += 1

    def on_touch_down(self, touch):
        bead = None
        for child in self.children:
            if child.collide_point(*touch.pos):
                bead = child
                break
        if bead is None:
            return False
        touch.ud['bead'] = bead
        touch.grab(self)

    def on_touch_move(self, touch):
        if touch.ud.has_key('bead'):
            dy = touch.y - touch.py
            touch.ud['bead'].move_by(dy)


class Bead(Widget):
    def move_by(self, dy):
        self.relax()
    def relax(self, dy):
        pass


class SorobanApp(App):
    def build(self):
        bs = BeadSlider()
        bs.beads = 2
        Clock.schedule_once(bs.reset_beads, 3)
        return bs

if __name__ == "__main__":
    SorobanApp().run()
