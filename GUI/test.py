# using:utf-8
from kivy.config import Config
Config.set("graphics", "width", "640")
Config.set("graphics", "height", "480")

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.properties import StringProperty, ListProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path

resource_add_path("./fonts")
LabelBase.register(DEFAULT_FONT, "Hannari.otf")

class TextWidget(Widget):
    text = StringProperty()

    def __init__(self, **kwargs):
        super(TextWidget, self).__init__(**kwargs)
        self.text = ""

    def buttonClicked(self):
        if self.text == "ハロー":
            self.text = "はんなりフォント"
        else:
            self.text = "ハロー"

class TestApp(App):
    
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = "Test App"
    
    def build(self):
        return TextWidget()
    
TestApp().run()
