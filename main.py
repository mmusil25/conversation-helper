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
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.properties import StringProperty
from kivy.lang import Builder
sent_analysis = pipeline("sentiment-analysis")

class ScrollableLabel(ScrollView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ScrollView does not allow us to add more than one widget, so we need to trick it
        # by creating a layout and placing two widgets inside it
        # Layout is going to have one collumn and and size_hint_y set to None,
        # so height wo't default to any size (we are going to set it on our own)
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        # Now we need two wodgets - Label for chat history and 'artificial' widget below
        # so we can scroll to it every new message and keep new messages visible
        # We want to enable markup, so we can set colors for example
        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()

        # We add them to our layout
        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    # Methos called externally to add new message to the chat history
    def update_chat_history(self, message):

        # First add new line and message itself
        self.chat_history.text += '\n' + message

        # Set layout height to whatever height of chat history text is + 15 pixels
        # (adds a bit of space at teh bottom)
        # Set chat history label to whatever height of chat history text is
        # Set width of chat history text to 98 of the label width (adds small margins)
        self.layout.height = self.chat_history.texture_size[1] + 15
        self.chat_history.height = self.chat_history.texture_size[1]
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)

        # As we are updating above, text height, so also label and layout height are going to be bigger
        # than the area we have for this widget. ScrollView is going to add a scroll, but won't
        # scroll to the botton, nor there is a method that can do that.
        # That's why we want additional, empty wodget below whole text - just to be able to scroll to it,
        # so scroll to the bottom of the layout
        self.scroll_to(self.scroll_to_point)


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
        self.interlocuteur = TextInput(multiline=True, font_size = 13, size_hint=(1, .1))
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
