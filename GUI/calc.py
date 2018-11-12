# using:utf-8
from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.utils import get_color_from_hex
from kivy.resources import resource_add_path

from kivy.factory import Factory

resource_add_path("./fonts")
LabelBase.register(DEFAULT_FONT, "Hannari.otf")

class Calculator1(BoxLayout):
    clear_bool = BooleanProperty(False)
    
    def print_number(self, number):

        if self.clear_bool: 
            self.clear_display()

        text = "{}{}".format(self.display.text, number)
        self.display.text = text

        print("数字 {0} が押されました".format(unmber))

    def print_operator(self, operator):
        if self.clear_bool:
            self.clear_bool = False


class CalculatorApp(App):
    def __init__(self, **kwargs):
        super(CalculatroApp, self).__init__(**kwargs)

        self.title = "電卓"
    pass

if __name__ == "__main__":
    Window.clearcolor = get_color_from_hex("#FFFFFF")
    CalculatorApp().run()
