# conversation-helper

With the shift to a mobile first life, new friends are often made through apps. Unfortunately these apps tend to freeze the air between the two interlocuteurs before they find a topic they can riff off. 

Modern tools can be configured to help. Tools like Tinder chatbots are all too common and leave no room for personality to shine through or unique connections to emerge. A middle ground is needed where ML models can be used to assist the forming of social bonds by helping to overcome common conversational hiccups. Made with <3 by [Mark](https://www.markmusil.com/)

## Use Case

The most common use case for this tool is for getting-to-know-you conversations that are at risk of losing their energy. Take this Bumble BFF match for example. I asked a "How are You" type question and received a similar response. Often, I find that I will fail to reply to messages that lose my interest. The transformer adds the spontaneity needed to keep the conversation going. 


![bumble](media/bumble.png)

## Upcoming Release Improvements
* Conversation logging
* Display conversational meta information (greeting, question, suggestion, statement, etc.) and likelihood of a certain meta token for a given draft message. 
* Hyperparameter tuning via the GUI
* Sentiment analysis for your drafted message
* Bayesian prediction of how they will reply based on their previous replies 

## Usage

Install dependencies via requirements.txt

```
pip install -r requirements.txt
```

Run GUI.py and follow the instructions printed at start up :)

```
python3 GUI.py
```

For the experimental release (where I'm doing most of my hyperparameter tuning and experimentation)

```
python3 main.py
```
## Credit to the following online resources

[How to generate text: using different decoding methods for language generation with Transformers](https://huggingface.co/blog/how-to-generate)

[Conversational AI Chatbot with Transformers in Python](https://www.thepythoncode.com/article/conversational-ai-chatbot-with-huggingface-transformers-in-python)
