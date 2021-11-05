from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import yake
from transformers import pipeline
from craigslist_scraper.scraper import scrape_url
import threaded
import concurrent
from win10toast import ToastNotifier
n = ToastNotifier()
QT = True
if QT:
    import PySimpleGUIQt as sg
else:
    import PySimpleGUI as sg

text_list = [
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large",
    "gpt2"
]

moods = [
    "normal, reserved, friendly",
    "spontaneous, random, assertive",
]

mood_levels = {
    1: "normal, reserved, friendly",
    2: "spontaneous, random, assertive",
}

sent_analysis = pipeline("sentiment-analysis")

@threaded.ThreadPooled
def analyze_and_print(text, window):
    result = sent_analysis(text)[0]
    window['-MLINE-'].update(f"\n\nLabel:  {result['label']}\n", append=True, autoscroll=True)
    window['-MLINE-'].update(f"Confidence:  {result['score']}\n\n", append=True, autoscroll=True)
    return

concurrent.futures.wait([analyze_and_print()])

def process_urls(url, window=None, model=None, tokenizer=None, gen_dict = None, chat_history_ids_list=None):
    data = scrape_url(url)
    window['-MLINE-'].update(data.title + "\n", append=True, autoscroll=True)
    info = data.the_whole_post()
    window['-MLINE-'].update(info, append=True, autoscroll=True)
    analyze_and_print(info, window)

    kw_extractor = yake.KeywordExtractor()
    language = "en"
    max_ngram_size = 3
    deduplication_threshold = 0.9
    numOfKeywords = 20
    custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                                     top=numOfKeywords, features=None)
    keywords = custom_kw_extractor.extract_keywords(info)
    my_gpt2_string = ""
    window['-MLINE-'].update(f"\n Keywords from this post:", append=True, autoscroll=True)
    for kw in keywords:
        my_gpt2_string += (kw[0] + " ")
        window['-MLINE-'].update(f"{kw[0]}", append=True, autoscroll=True)

    chat_history_ids_list, bot_input_ids = magic_machine_learning_function(my_gpt2_string, chat_history_ids_list,
                                                                           window, model, tokenizer, gen_dict)
    window['-MLINE-'].update("\nTry saying one of the following to break the ice.\n\n", append=True, autoscroll=True)
    for i, option in enumerate(chat_history_ids_list):
        output = tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
        window['-MLINE-'].update(f"{i}: {output}", append=True, autoscroll=True)
        window['-MLINE-'].update("\n", append=True, autoscroll=True)

    chat_history_ids_list = tokenizer.encode(data.the_whole_post() + tokenizer.eos_token, return_tensors="pt")
    window['-MLINE-'].update(f"\n\nEnter their reply\n", append=True, autoscroll=True)
    window['-MLINE-'].update("\n", append=True, autoscroll=True)
    return  chat_history_ids_list





def call_and_response(gen_dict, tokenizer, model, window, text ,exchanges=1, chat_history_ids_list = None):
    for step in range(exchanges):
        window['-MLINE-'].update("\nEncoding inputs...\n", append=True, autoscroll=True)
        inputs_ids = tokenizer.encode(text+tokenizer.eos_token, return_tensors="pt")
        try:
            window['-MLINE-'].update("\nBuilding conversation history...\n", append=True, autoscroll=True)
            bot_input_ids = torch.cat([chat_history_ids_list, inputs_ids], dim= -1) if step > 0 else inputs_ids
        except:
            continue

        window['-MLINE-'].update("\nGenerating model outputs...\n", append=True, autoscroll=True)

        chat_history_ids_list = model.generate(
            bot_input_ids,
            **gen_dict

        )
    return chat_history_ids_list, bot_input_ids

@threaded.ThreadPooled
def magic_machine_learning_function(message, chat_history_ids_list, window, model, tokenizer, gen_dict):
    chat_history_ids_list, bot_input_ids= call_and_response(gen_dict, tokenizer, model, window, message, exchanges=1,
                                                            chat_history_ids_list=chat_history_ids_list)
    return chat_history_ids_list, bot_input_ids
concurrent.futures.wait([magic_machine_learning_function()])

def entry_point():

    # Create some elements
    layout = [
            [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
            [sg.T('Message> '), sg.Input(key='-IN-', focus=True, do_not_clear=False)],
            [sg.Button('Input', bind_return_key=True), sg.Button('Close')],
            [sg.Text('Select a Model:')],
            [sg.Listbox(values=text_list,
                     size=(400, 20 * len(text_list)) if QT else (15, len(text_list)),
                     change_submits=True,
                     bind_return_key=True,
                     auto_size_text=True,
                     default_values=text_list[2],
                     key='_FLOATING_LISTBOX_', enable_events=True)],
            [sg.Text('Select a mood:')],
            [sg.Listbox(values=moods,
                    size=(400, 20 * len(moods)) if QT else (15, len(moods)),
                    change_submits=True,
                    bind_return_key=True,
                    auto_size_text=True,
                    default_values="normal, reserved, friendly",
                    key='-MOOD-', enable_events=True)],
            [sg.T('Enter a craiglist URL> '), sg.Input(key='-IN_Craig-', focus=True, do_not_clear=False)],
            [sg.Button('Should I buy?', bind_return_key=False)],

    ]
    # Create the Window
    window = sg.Window('Conversation Helper', layout, finalize=True)
    # Create the event loop
    chat_history_ids_list = []
    version_string = "0.1"
    welcome_string = f"\n\n" \
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
    window['-MLINE-'].update(welcome_string, append=True, autoscroll=True)
    window['-MLINE-'].update("", append=True, autoscroll=True)

    while True:
        event, values = window.read()
        try:
            if event == 'Close':
                # User closed the Window or hit the Cancel button
                break
            elif event is None:
                break
            elif event == 'Input' or 'Should I buy?':
                model_name = values['_FLOATING_LISTBOX_'][0]

                tokenizer = AutoTokenizer.from_pretrained(model_name)

                if values['-MOOD-'][0] == mood_levels[2]:
                    gen_dict = {
                        "max_length": 200000,
                        "do_sample": True,
                        "top_p": 0.95,
                        "top_k": 100,
                        "temperature": 0.7,
                        "num_return_sequences": 10,
                        "pad_token_id": tokenizer.eos_token_id,
                        "num_beams": 2
                    }
                if values['-MOOD-'][0] ==  mood_levels[1]:
                    gen_dict = {
                        "max_length": 200000,
                        "do_sample": True,
                        "top_p": 0.95,
                        "top_k": 100,
                        "temperature": 1,
                        "num_return_sequences": 10,
                        "pad_token_id": tokenizer.eos_token_id,
                        "num_beams": 2
                    }

                model = AutoModelForCausalLM.from_pretrained(model_name)

                # window['-MLINE-'].update(f"\nThey said: {values['-IN-']}\n", append=True, autoscroll=True)
                # window['-MLINE-'].update("\nRunning magical machine learning box... \n", append=True, autoscroll=True)
                if event == 'Input':
                    chat_history_ids_list, bot_input_ids = magic_machine_learning_function(values['-IN-'], chat_history_ids_list, window, model,tokenizer, gen_dict)
                    window['-MLINE-'].update("\nTry saying one of the following.\n\n", append=True, autoscroll=True)
                    for i, option in enumerate(chat_history_ids_list):
                        output = tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
                        window['-MLINE-'].update(f"{i}: {output}", append=True, autoscroll=True)
                        window['-MLINE-'].update("\n", append=True, autoscroll=True)

                    chat_history_ids_list = tokenizer.encode(values['-IN-'] + tokenizer.eos_token, return_tensors="pt")
                    window['-MLINE-'].update(f"\n\nEnter their reply\n", append=True, autoscroll=True)
                    window['-MLINE-'].update("\n", append=True, autoscroll=True)

                    n.show_toast("Replies ready", "Now you know what to say.", duration=10,
                                 icon_path=r"media\notice.ico")
                elif event == 'Should I buy?':
                    chat_history_ids_list = process_urls(values['-IN_Craig-'], model=model, tokenizer=tokenizer,
                                                       gen_dict = gen_dict,
                                 window=window, chat_history_ids_list=chat_history_ids_list)



        except Exception as e:
            sg.popup_error(f"Oh no an exception occurred: {e}")
            continue

    window.close()


if __name__ == '__main__':
    entry_point()