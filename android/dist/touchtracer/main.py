from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
# GridLayout arranges children in a matrix.
from kivy.uix.gridlayout import GridLayout
# Label is used to label something
from kivy.uix.label import Label
# used to take input from users
import random
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from GUI import *



model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
gen_dict = {
                        "max_length": 2000,
                        "do_sample": True,
                        "top_p": 0.95,
                        "top_k": 100,
                        "temperature": 0.7,
                        "num_return_sequences": 10,
                        "pad_token_id": tokenizer.eos_token_id
                    }
red = [1,0,0,1]
green = [0,1,0,1]

class MainApp(App):

    def build(self):
        # label = Label(text='Hello from Kivy',
        #               size_hint=(.5, .5),
        #               pos_hint={'center_x': .5, 'center_y': .5})
        #
        # return label
        layout = BoxLayout(padding=30, orientation="vertical")

        self.input_line = TextInput(multiline=False, readonly=False, halign="right", font_size=44)
        layout.add_widget(self.input_line)

        btn = Button(text="Enter", background_color=green)
        layout.add_widget(btn)
        btn.bind(on_press=self.on_press_button)
        return layout

    def on_press_button(self, instance):
        print(self.input_line.text) # On button press, read in the user's input.

class ButtonApp(App):
    def build(self):

        return Button()

    def on_press_button(self):
        print('You pressed the button!')

def ML_function(text, chat_history_ids_list, model, tokenizer, gen_dict):
    inputs_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    bot_input_ids = torch.cat([chat_history_ids_list, inputs_ids], dim=-1) if len(chat_history_ids_list) > 0 else inputs_ids
    chat_history_ids_list = model.generate(
        bot_input_ids,
        **gen_dict
    )
    return chat_history_ids_list, bot_input_ids


class LoginScreen(BoxLayout):
    def __init__(self, **var_args):
        super(LoginScreen, self).__init__(**var_args)
        # super function can be used to gain access
        # to inherited methods from a parent or sibling class
        # that has been overwritten in a class object.
        self.padding = 100
        self.orientation = 'vertical'
        self.mytext = ""

        self.lbl = Label(text=self.mytext, size_hint=(.5, .5),
                       pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.lbl)
        self.add_widget(Label(text='Message>', size_hint=(.5, .5),
                       pos_hint={'center_x': .5, 'center_y': .1}))
        self.interlocuteur = TextInput(multiline=True, font_size = 13, size_hint=(.5, .5))
        self.add_widget(self.interlocuteur)
        self.btn = Button(text="Enter", background_color = green, font_size = 13, size_hint=(.5, .5))
        self.add_widget(self.btn)
        self.btn.bind(on_press=self.on_button_press)
    def on_button_press(self, instance):
        self.lbl.text = ""
        chat_history_ids_list = []
        chat_history_ids_list, bot_input_ids = ML_function(self.interlocuteur.text,
                                                           chat_history_ids_list,
                                                           model, tokenizer, gen_dict)
        for i, option in enumerate(chat_history_ids_list):
            output = tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
            self.lbl.text += output
            self.lbl.text += "\n"

        self.interlocuteur.text = ""




# the Base Class of our Kivy App
class MyApp(App):
    def build(self):
        # return a LoginScreen() as a root widget
        return LoginScreen()


if __name__ == '__main__':
    MyApp().run()
