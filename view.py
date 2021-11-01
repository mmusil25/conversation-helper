#docs
# https://pysimplegui.readthedocs.io/en/latest/call%20reference/

from model import Model
import PySimpleGUIQt as sg
import win10toast as wt

moods = [
    "normal, reserved, friendly",
    "spontaneous, random, assertive",
]
text_list = [
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
    "gpt2"
]
mood_levels = {
    "normy": moods[0],
    "punk": moods[1],
}
version_string = "0.1"
QT = True
class View:
    def __init__(self, view_choice):

        self.frame_work = view_choice
        self.model = Model()
        self.reroll_text = "Hi :)"
        self.notice_maker = wt.ToastNotifier()

        if self.frame_work == "PySimpleGUIQt":
            self.layout = [
            [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
            [sg.T('Message > '), sg.Input(default_text = "Hello! How are you?", key='-IN-', focus=True, do_not_clear=False, )],
            [sg.Button('Input', bind_return_key=True), sg.Button('Cancel')],
            [sg.Text('Select a Model:')],
            [sg.Listbox(values=text_list,
                     size=(400, 20 * len(text_list)) if QT else (15, len(text_list)),
                     change_submits=True,
                     bind_return_key=True,
                     auto_size_text=True,
                     default_values=text_list[0],
                     key='_FLOATING_LISTBOX_', enable_events=True)],
            [sg.Text('Select a mood:')],
            [sg.Listbox(values=moods,
                    size=(400, 20 * len(moods)) if QT else (15, len(moods)),
                    change_submits=True,
                    bind_return_key=True,
                    auto_size_text=True,
                    default_values="normal, reserved, friendly",
                    key='-MOOD-', enable_events=True)],
                ]
            self.window = sg.Window('Conversation Helper', self.layout, finalize=True)
            self.version_string = "0.1"
            self.welcome_string = f"\n\n" \
                     f" ***************************************\n" \
                     f" Conversation Helper v" + version_string + " \n" \
                     f" ***************************************\n" \
                     f"Do you wish you always knew what to say? Enter the Conversation Helper! This program uses GPT to suggest " \
                     f"responses in conversations. By entering further replies, your answers will improve as the conversation flows. " \
                     f"\n\nMade with <3 - https://github.com/mmusil25/conversation-helper" \
                     f"\n\n\n" \
                     f" Enter the message from your conversation partner"\
                     " to receive suggested replies. Once you've chosen a reply or used your own, have sent the reply, and have received a response, Enter their " \
                     "reply to receive a new batch of contextual responses based on previous messages. \n"\
                     "\n(Note: This is a very large transformer and may appear to freeze. Please be patient.) \n" \
                      "\n Try it! Enter their message in the white prompt box below.\n\n\n"
            self.window['-MLINE-'].update(self.welcome_string, append=True, autoscroll=True)
            self

    def mood_selector(self, choice):
        if choice == mood_levels[2]:
            gen_dict = {
                "max_length": 200000,
                "do_sample": True,
                "top_p": 0.95,
                "top_k": 100,
                "temperature": 0.7,
                "num_return_sequences": 10,
                "pad_token_id": self.tokenizer.eos_token_id,
                "num_beams": 2
            }
        elif choice ==  mood_levels[1]:
            gen_dict = {
                "max_length": 200000,
                "do_sample": True,
                "top_p": 0.95,
                "top_k": 100,
                "temperature": 1,
                "num_return_sequences": 10,
                "pad_token_id": self.tokenizer.eos_token_id,
                "num_beams": 2
                                }
        return gen_dict

    def PySimpleGUI_main_loop(self):
        while True:
            event, values = self.window.read()
            self.reroll_text = values["-IN-"]
            try:
               
                if event is None:
                    break
                elif event == 'Reroll':
                    break
                elif event == 'Input':
                    model_name = values['_FLOATING_LISTBOX_'][0]
                    self.model.setmodel(model_name)
                    gen_dict = self.mood_selector(values['-MOOD-'][0])
                    self.window['-MLINE-'].update(f"\nThey said: {values['-IN-']}\n", append=True, autoscroll=True)
                    self.window['-MLINE-'].update("\nTry saying one of the following.\n\n", append=True,
                                                  autoscroll=True)
                    for i, option in enumerate(5):
                        magic_answer = self.model.call_and_response(values['-IN-'], gen_dict)
                        self.window['-MLINE-'].update(f"{i}: {magic_answer}", append=True, autoscroll=True)
                        self.window['-MLINE-'].update("\n", append=True, autoscroll=True)
                        self.notice_maker.show_toast(f"Reply number {i} ready", duration=1,icon_path=r"media\notice.ico")

                    self.window['-MLINE-'].update(f"\n\nEnter their reply\n", append=True, autoscroll=True)
                    self.window['-MLINE-'].update("\n", append=True, autoscroll=True)

            except Exception as e:
                sg.popup_error(f"Oh no an exception occurred: {e}")
                continue
