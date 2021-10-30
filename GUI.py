import PySimpleGUI as sg
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datasets import load_metric
import numpy as np
import notifypy

metric = load_metric("accuracy")
model_name = "microsoft/DialoGPT-large"

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
except:
    tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(model_name)
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


def call_and_response(text ,exchanges=1, chat_history_ids_list = None):
    for step in range(exchanges):
        #text = input(">> Conversational Partner: ")
        inputs_ids = tokenizer.encode(text+tokenizer.eos_token, return_tensors="pt")
        try:
            bot_input_ids = torch.cat([chat_history_ids_list, inputs_ids], dim= -1) if step > 0 else inputs_ids
        except:
            continue

        chat_history_ids_list = model.generate(
            bot_input_ids,
            max_length = 2000,
            do_sample=True,
            top_p=0.95,
            top_k=100,
            temperature=1,
            num_return_sequences=10,
            pad_token_id = tokenizer.eos_token_id
        )
        #print("Suggested responses to what they sent you: ")

            #print(f"{i}: {output}")

    return chat_history_ids_list, bot_input_ids

def magic_machine_learning_function(message, chat_history_ids_list):
    chat_history_ids_list, bot_input_ids= call_and_response(message, exchanges=1, chat_history_ids_list=chat_history_ids_list)
    return chat_history_ids_list, bot_input_ids


def entry_point():
    import torch
    # Create some elements
    layout = [
            [sg.Multiline(size=(110, 30), font='courier 10', background_color='black', text_color='white', key='-MLINE-')],
            [sg.T('Message> '), sg.Input(key='-IN-', focus=True, do_not_clear=False)],
            [sg.Button('Input', bind_return_key=True), sg.Button('Cancel')]
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
                     f"you can't think of what to say :) Made with <3 by Mark - https://www.linkedin.com/in/mark-musil/" \
                     f"\n\n\n" \
                     f" Enter the message from your conversation partner"\
                     " to receive suggested replies. Once you've chosen a reply or used your own, have sent the reply, and have received a response, Enter their " \
                     "reply to receive a new batch of contextual responses based on previous messages. \n"\
                     "\n Try it! Enter their message in the white prompt box below.\n\n\n"
    #window.read()
    window['-MLINE-'].update(welcome_string)

    while True:

        try:
            if event == 'Exit':
                # User closed the Window or hit the Cancel button
                break
            elif event == 'Input':
                window['-MLINE-'].update(f"\nThey said: {values['-IN-']}\n", append=True, autoscroll=True)
                chat_history_ids_list, bot_input_ids = magic_machine_learning_function(values['-IN-'], chat_history_ids_list)
                window['-MLINE-'].update("\nTry saying one of the following.\n", append=True, autoscroll=True)
                for i, option in enumerate(chat_history_ids_list):
                    output = tokenizer.decode(chat_history_ids_list[i][bot_input_ids.shape[-1]:], skip_special_tokens=True)
                    window['-MLINE-'].update(f"{i}: {output}", append=True, autoscroll=True)
                    window['-MLINE-'].update("\n\n\n", append=True, autoscroll=True)

                window['-MLINE-'].update(f"\nEnter their reply\n", append=True, autoscroll=True)
                window['-MLINE-'].update("\n", append=True, autoscroll=True)

                choice_index = int(values['-IN-'])
                chat_history_ids_list = torch.unsqueeze(chat_history_ids_list[choice_index], dim=0)

        except:
            event, values = window.read()
    window.close()

if __name__ == '__main__':
    entry_point()