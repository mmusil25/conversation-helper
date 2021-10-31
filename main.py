#credit https://www.thepythoncode.com/article/conversational-ai-chatbot-with-huggingface-transformers-in-python
from win10toast import ToastNotifier
n = ToastNotifier()

import kivy
kivy.require('2.0.0')
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import pipeline
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder
sent_analysis = pipeline("sentiment-analysis")



class LoginScreen(BoxLayout):
    def __init__(self, **var_args):
        super(LoginScreen, self).__init__(**var_args)
        # super function can be used to gain access
        # to inherited methods from a parent or sibling class
        # that has been overwritten in a class object.
        self.padding = 100
        self.orientation = 'vertical'
        self.mytext = ""
        self.reroll_text = "Hi ;)"
        #self.model_name = "microsoft/DialoGPT-medium"
        self.model_name = "microsoft/DialoGPT-large"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.gen_dict = {
            #https://huggingface.co/transformers/main_classes/model.html?highlight=generate
            "max_length": 30000,
            "do_sample": True,
            "top_p": 0.95,
            "top_k": 100,
            "temperature": 0.6,
            "num_return_sequences": 5,
            "pad_token_id": self.tokenizer.eos_token_id
        }
        green = [0, 1, 0, 1]

        self.lbl = Label(font_size=14)
        self.add_widget(self.lbl)
        #self.add_widget(Label(text='Message>', size_hint=(.5, .5),
         #              pos_hint={'center_x': .5, 'center_y': .1}))
        self.interlocuteur = TextInput(multiline=True, font_size = 13, size_hint=(1, .4))
        self.add_widget(self.interlocuteur)
        self.btn = Button(text="Enter", background_color = green, font_size = 13, size_hint=(.3, .1))
        self.add_widget(self.btn)
        self.btn.bind(on_press=self.on_button_press)

        self.btn2 = Button(text="New Answer", background_color="purple", font_size=13, size_hint=(.3, .1))
        self.add_widget(self.btn2)
        self.btn2.bind(on_press=self.send_reroll)

    def send_reroll(self, instance):
        self.lbl.text = ""
        self.lbl.text = "Loading"
        chat_history_ids_list = []
        chat_history_ids_list, bot_input_ids = self.ML_function(self.reroll_text,
                                                                chat_history_ids_list,
                                                                self.model, self.tokenizer, self.gen_dict)
        #self.lbl.text = "\n\nThey Said: " + self.interlocuteur.text + "\n\n"
        self.lbl.text = ""
        for i, option in enumerate(chat_history_ids_list):
            output = self.tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
            result = sent_analysis(output)[0]
            # "Confidence score: {result['score']}"
            self.lbl.text += (output + f" \n Label: {result['label']} - Confidence score:"
                                       f" {round(result['score'] * 100)}\n\n")

        self.interlocuteur.text = ""
        n.show_toast("Replies ready", "Now you know what to say.", duration=10,
                     icon_path=r"media\notice.ico")

    def on_button_press(self, instance):
        self.lbl.text = ""
        self.lbl.text = "Loading"
        chat_history_ids_list = []
        chat_history_ids_list, bot_input_ids = self.ML_function(self.interlocuteur.text,
                                                           chat_history_ids_list,
                                                           self.model, self.tokenizer, self.gen_dict)
        #self.lbl.text = "\n\nThey Said: " + self.interlocuteur.text + "\n\n"
        self.lbl.text = ""
        for i, option in enumerate(chat_history_ids_list):
            output = self.tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
            result = sent_analysis(output)[0]
            # "Confidence score: {result['score']}"
            self.lbl.text += (output + f" \n Label: {result['label']} - Confidence score:"
                                                      f" {round(result['score']*100)}\n\n")
        self.reroll_text = self.interlocuteur.text
        self.interlocuteur.text = ""
        n.show_toast("Replies ready", "Now you know what to say.", duration=10,
                     icon_path=r"media\notice.ico")

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