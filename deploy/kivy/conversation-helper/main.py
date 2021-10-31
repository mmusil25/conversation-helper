import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch







class LoginScreen(BoxLayout):
    def __init__(self, **var_args):
        super(LoginScreen, self).__init__(**var_args)
        # super function can be used to gain access
        # to inherited methods from a parent or sibling class
        # that has been overwritten in a class object.
        self.padding = 100
        self.orientation = 'vertical'
        self.mytext = ""
        self.model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.gen_dict = {
            "max_length": 2000,
            "do_sample": True,
            "top_p": 0.90,
            "min_length": 20,
            "num_beams": 3,
            "top_k": 200,
            "repetition_penalty": 2,
            "length_penalty": 1.1,
            "temperature": 0.7,
            "num_return_sequences": 10,
            "pad_token_id": self.tokenizer.eos_token_id
        }
        red = [1, 0, 0, 1]
        green = [0, 1, 0, 1]

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
        chat_history_ids_list, bot_input_ids = self.ML_function(self.interlocuteur.text,
                                                           chat_history_ids_list,
                                                           self.model, self.tokenizer, self.gen_dict)
        for i, option in enumerate(chat_history_ids_list):
            output = self.tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
            self.lbl.text += output
            self.lbl.text += "\n"

        self.interlocuteur.text = ""

    def ML_function(self, text, chat_history_ids_list, model, tokenizer, gen_dict):
        inputs_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
        bot_input_ids = torch.cat([chat_history_ids_list, inputs_ids], dim=-1) if len(
            chat_history_ids_list) > 0 else inputs_ids
        chat_history_ids_list = model.generate(
            bot_input_ids,
            **gen_dict
        )
        return chat_history_ids_list, bot_input_ids



# the Base Class of our Kivy App
class MyApp(App):
    def build(self):
        # return a LoginScreen() as a root widget
        return LoginScreen()


MyApp().run()
