from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
import random
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

class MainApp(App):
    def build(self):
        # label = Label(text='Hello from Kivy',
        #               size_hint=(.5, .5),
        #               pos_hint={'center_x': .5, 'center_y': .5})
        #
        # return label
        #
        # img = Image(source=r'C:\Users\musil\source\repos\conversation-helper\media\hawaii.jpg',
        #             size_hint=(1, .5),
        #             pos_hint={'center_x': .5, 'center_y': .5})
        #
        # return img
        layout = BoxLayout(padding=30, orientation="vertical")
        colors = [red, green, blue, purple]

        for i in range(5):
            btn = Button(text="Button #%s" % (i + 1),
                         background_color=random.choice(colors)
                         )

            layout.add_widget(btn)
        return layout

if __name__ == '__main__':
    app = MainApp()
    app.run()