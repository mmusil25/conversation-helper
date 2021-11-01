from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from transformers import pipeline






# Instantiate the shared pipeline tools

class Model:
    def __init__(self, ):
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.chat_history_ids_list = []
        self.input_ids = []
        self.bot_inputs_ids = []
        return

    def setmodel(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)


        self.vanilla_gen_dict = {
                        "max_length": 200000,
                        "do_sample": True,
                        "top_p": 0.95,
                        "top_k": 100,
                        "temperature": 0.7,
                        "num_return_sequences": 10,
                        "pad_token_id": self.tokenizer.eos_token_id,
                        "num_beams": 2
                    }
        return
    
    def call_and_response(self,text,gen_dict):
        #Encode our text input and add an end of string token to it. 
        inputs_ids = self.tokenizer.encode(text+self.tokenizer.eos_token, return_tensor="pt")
        # Build a chat history by adding the new message to the tokenized history list. 
        bot_inputs_ids = torch.cat([self.chat_history_ids_list, self.input_ids], dim=-1)
        self.chat_history_ids_list = self.model.generate(bot_inputs_ids, **gen_dict)
        output = self.tokenizer.decode(self.chat_history_ids_list[0][self.bot_input_ids.shape[-1]:],
                                  skip_special_tokens=True)
        return output