import kivy, os, sys
from kivy.config import Config
Config.set('graphics', 'resizable', '0')
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from gui.widgets_config import MainLayout

# Window config, app was intended to be used in 960x540 resolution
kivy.require('2.3.1')
Window.size = (960, 540)
Window.clearcolor = (0.078, 0.078, 0.078, 1)
Window.set_icon(os.path.join('resource', 'img', 'img_lp.png'))

class MinimalystApp(App):
    def build(self):
        def resource_path(relative_path):
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            return os.path.abspath(relative_path)
        Builder.load_file(resource_path(os.path.join('gui', 'minimalyst.kv')))
        return MainLayout()

ui = MinimalystApp()
ui.run()