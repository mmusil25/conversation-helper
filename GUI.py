from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datasets import load_metric
import numpy as np
import notifypy
QT = True
if QT:
    import PySimpleGUIQt as sg
else:
    import PySimpleGUI as sg

text_list = [
    "microsoft/DialoGPT-medium",
    "microsoft/DialoGPT-large"

]

mood_levels = [
    "normal, reserved, friendly",
    "spontaneous, random, assertive"
]


#model = AutoModelForSequenceClassification.from_pretrained(r"D:\GoogleDrive\Personal\Hobbies Fun and Interests\Programming\python\NLP\TinderChatBot\model_saves", num_labels=2)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

def tokenize_function(examples):
    return tokenizer(examples["text"],padding="max_length", truncation=True)

def fine_tune():
    raw_datasets = load_dataset("imdb")
    print(f"IMDB dataset columns: {raw_datasets.column_names}")

    #inputs = tokenizer(sentences, padding="max_length", truncation=True)
    tokenized_datasets = raw_datasets.map(tokenize_function, batched=True)

    small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
    small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(1000))
    full_train_dataset = tokenized_datasets["train"]
    full_eval_dataset = tokenized_datasets["test"]

    from transformers import TrainingArguments
    training_args = TrainingArguments("test_trainer")

    from transformers import Trainer
    #trainer= Trainer(model=model, args=training_args, train_dataset=small_train_dataset, eval_dataset=small_eval_dataset)

    #trainer.train()
    training_args = TrainingArguments("test_trainer", evaluation_strategy="epoch")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
        compute_metrics=compute_metrics,
    )
    trainer.evaluate()
    import os
    trainer.save_model(r"D:\GoogleDrive\Personal\Hobbies Fun and Interests\Programming\python\NLP\TinderChatBot\model_saves")
    print("Model saved")
    notice = notifypy.Notify()
    notice.title = "Training Done"
    notice.message = "The model is done training"
    notice.send()
    from transformers import TrainingArguments


def call_and_response(gen_dict, tokenizer, model, window, text ,exchanges=1, chat_history_ids_list = None):
    for step in range(exchanges):
        #text = input(">> Conversational Partner: ")
        window['-MLINE-'].update("\nEncoding inputs...\n", append=True, autoscroll=True)
        inputs_ids = tokenizer.encode(text+tokenizer.eos_token, return_tensors="pt")
        try:
            window['-MLINE-'].update("\nBuilding conversation using previous replies...\n", append=True, autoscroll=True)
            bot_input_ids = torch.cat([chat_history_ids_list, inputs_ids], dim= -1) if step > 0 else inputs_ids
        except:
            continue

        window['-MLINE-'].update("\nGenerating model outputs...\n", append=True, autoscroll=True)

        chat_history_ids_list = model.generate(
            bot_input_ids,
            **gen_dict

        )
        #print("Suggested responses to what they sent you: ")

            #print(f"{i}: {output}")

    return chat_history_ids_list, bot_input_ids

def magic_machine_learning_function(message, chat_history_ids_list, window, model, tokenizer, gen_dict):
    chat_history_ids_list, bot_input_ids= call_and_response(gen_dict, tokenizer, model, window, message, exchanges=1, chat_history_ids_list=chat_history_ids_list)
    return chat_history_ids_list, bot_input_ids


def entry_point():
    import torch
    # Create some elements
    layout = [
            [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
            [sg.T('Message> '), sg.Input(key='-IN-', focus=True, do_not_clear=False)],
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
            [sg.Listbox(values=mood_levels,
                    size=(400, 20 * len(mood_levels)) if QT else (15, len(mood_levels)),
                    change_submits=True,
                    bind_return_key=True,
                    auto_size_text=True,
                    default_values=mood_levels[0],
                    key='-MOOD-', enable_events=True)],
              ]
    # Create the Window
    window = sg.Window('Conversation Helper', layout, finalize=True)
    # Create the event loop
    chat_history_ids_list = []
    bot_input_ids = []
    version_string = "0.1"
    welcome_string = f"\n\n" \
                     f" ***************************************\n" \
                     f" Conversation Helper v" + version_string + " \n" \
                     f" ***************************************\n" \
                     f"\n Have you ever had trouble knowing what to reply? " \
                     f"Do you wish you always knew what to say? Enter the Conversation Helper! This program uses GPT to suggest " \
                     f"responses in conversations. By entering further replies, your answers will improve as the conversation flows. " \
                     f"These suggestions are not meant to substitute empathy and are more of a starting point when " \
                     f"you can't think of what to say :) Made with <3 - https://github.com/mmusil25/conversation-helper" \
                     f"\n\n\n" \
                     f" Enter the message from your conversation partner"\
                     " to receive suggested replies. Once you've chosen a reply or used your own, have sent the reply, and have received a response, Enter their " \
                     "reply to receive a new batch of contextual responses based on previous messages. \n"\
                     "\n(Note: This is a very large transformer and may appear to freeze. Please be patient.) \n" \
                      "\n Try it! Enter their message in the white prompt box below.\n\n\n"
    #window.read()
    window['-MLINE-'].update(welcome_string)

    while True:
        event, values = window.read()
        try:
            if event == 'Cancel':
                # User closed the Window or hit the Cancel button
                break
            elif event is None:
                break
            elif event == 'Input':


                model_name = values['_FLOATING_LISTBOX_'][0]


                tokenizer = AutoTokenizer.from_pretrained(model_name)

                if values['-MOOD-'][0] == "normal, reserved, friendly":
                    gen_dict = {
                        "max_length": 2000,
                        "do_sample": True,
                        "top_p": 0.95,
                        "top_k": 100,
                        "temperature": 0.7,
                        "num_return_sequences": 10,
                        "pad_token_id": tokenizer.eos_token_id
                    }
                if values['-MOOD-'][0] == "spontaneous, random, assertive":
                    gen_dict = {
                        "max_length": 2000,
                        "do_sample": True,
                        "top_p": 0.95,
                        "top_k": 100,
                        "temperature": 1,
                        "num_return_sequences": 10,
                        "pad_token_id": tokenizer.eos_token_id
                    }

                model = AutoModelForCausalLM.from_pretrained(model_name)

                window['-MLINE-'].update(f"\nThey said: {values['-IN-']}\n", append=True, autoscroll=True)
                window['-MLINE-'].update("\nRunning magical machine learning box... \n", append=True, autoscroll=True)
                chat_history_ids_list, bot_input_ids = magic_machine_learning_function(values['-IN-'], chat_history_ids_list, window, model,tokenizer, gen_dict)
                window['-MLINE-'].update("\nTry saying one of the following.\n\n", append=True, autoscroll=True)
                for i, option in enumerate(chat_history_ids_list):
                    output = tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
                    window['-MLINE-'].update(f"{i}: {output}", append=True, autoscroll=True)
                    window['-MLINE-'].update("\n", append=True, autoscroll=True)

                window['-MLINE-'].update(f"\n\nEnter their reply\n", append=True, autoscroll=True)
                window['-MLINE-'].update("\n", append=True, autoscroll=True)

                choice_index = 1
                #chat_history_ids_list = torch.unsqueeze(chat_history_ids_list[choice_index], dim=0)
                chat_history_ids_list = tokenizer.encode(values['-IN-']+tokenizer.eos_token, return_tensors="pt")

        except Exception as e:
            sg.popup_error(f"Oh no an exception occurred: {e}")
            continue

    window.close()

if __name__ == '__main__':
    entry_point()