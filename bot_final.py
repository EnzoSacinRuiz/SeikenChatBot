from distutils.log import info
from email.message import Message
import os
import logging
import random
from unicodedata import name
import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
import random 
import json
import torch
from turtle import xcor
from model import NeuralNet
from seiken_nltk_bot import bag_of_words, stem,tokenize,calorias
import time
import pandas as pd



#Configurar logging
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()

#Solicitar TOKEN
TOKEN = os.getenv("TOKEN")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "databot.pth"

data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
palabras_totales = data["palabras_totales"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Seiken"

respuestas = ["Me alegro", "Genial crack", "Vale bro", "Chevere crack. Algo mas?"]


def start(update, context):
    logger.info(f" El usuario {update.effective_user['username']}, ha iniciado una conversacion")
    name = update.effective_user['first_name']
    update.message.reply_text(f"Hola {name} yo soy tu bot")

def random_number(update, context):
    user_id=update.effective_user['id']
    logger.info(f"El usuario {user_id}, ha solicitado un numero aleatorio")
    number=random.randint(0,10)
    context.bot.sendMessage(chat_id= user_id, parse_mode="HTML",text=f"<b>Numero</b> aleatorio: \n{number}")

def echo(update, context):
    user_id=update.effective_user['id']
    name = update.effective_user['first_name']
    # logger.info(f"El usuario {name} {user_id}, ha enviado un mensaje de texto")
    text = update.message.text

    df_conversacion = pd.Series()

    sentence = text
    logger.info(f"El usuario {name} {user_id} mandó: {[sentence]}")
    df_conversacion["nombre"] = name
    df_conversacion["user_id"] = user_id
    df_conversacion["mensaje"] = sentence
    if sentence == "calorias":
        calorias()
        time.sleep(5)

    sentence = tokenize(sentence)
    x = bag_of_words(sentence,palabras_totales)
    x = x.reshape(1,x.shape[0])
    x = torch.from_numpy(x).to(device)

    output = model(x)
    _, predicted = torch.max(output,dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output,dim = 1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                context.bot.sendMessage(
                    chat_id=user_id,
                    parse_mode = "MarkdownV2",
                    text = f"{random.choice(intent['responses'])} "
                )
    else:
        context.bot.sendMessage(
            chat_id=user_id,
            parse_mode = "MarkdownV2",
            text = f"{random.choice(respuestas)}"
        )
    print(df_conversacion)

if __name__=="__main__":
    my_bot = telegram.Bot(token=TOKEN)
    print(my_bot.getMe())


updater=Updater(my_bot.token, use_context=True)


#Creando un despachador
dp=updater.dispatcher

#Creando los manejadores
dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("random",random_number))
dp.add_handler(MessageHandler(Filters.text, echo))

updater.start_polling()
print("BOT LISTO")
updater.idle()