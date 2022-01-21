from matplotlib.style import context
import requests
import time 
import schedule
import random
import telegram
import os
import logging
import requests
import schedule
import telegram # pip install telegram
from schedule import every, repeat, run_pending
import threading
from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler
)


"""
Paso 1: Grupo de Telegram en donde se mandarán los mensajes https://t.me/+MZ6A91jsC_o1ZWIx
Paso 2: Crear Telegram Bot
Paso 3: Chat ID (-1001621138106)
Paso 4: API Bot http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/getUpdates
Paso 5: Mandar mensaje http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-628790056&text="Mensaje prueba"

"""


#### - BIBLIOTECA DE MENSAJES - ####

mensajes__motivacion_mañana = [

'El secreto para salir adelante es comenzar.¡A darle con todo!',
'La persona que serás en un futuro está determinada por lo que hagas hoy.', 
'No más excusas. Recuerda que, ¡sin esfuerzo no hay recompensa!',
'El dolor que sientes hoy es la fuerza que sentirás mañana.',
'Nunca renuncies a un sueño por el tiempo que tomará en conseguirlo. El tiempo pasará de todos modos.',
'La distancia entre los sueños y la realidad se llama disciplina.',
'La realidad es bastante simple, lo haces o no lo haces.',
'Cuida de tu cuerpo. Es el único lugar que tienes para vivir.',
'Un ganador es un perdedor que nunca se ha dado por vencido.',
'Las excusas queman 0 calorías por hora.', 'No tienes que estar “en forma” para iniciar, pero tienes que iniciar para estar en forma.',
'Nunca tires la toalla. Úsala para secar tu sudor y sigue adelante.',
'Más vale estar dolorido que arrepentido.',
'Cuando te sientas deprimido, sólo, estresado, triste, siempre hay una solución: ENTRENAR CON TODO.', 
'Cuando tus piernas y tu cabeza no puedan más... tu corazón hará el resto.',
'¿Qué hace una abeja en un gimnasio? Zumba.',
'La fuerza y el crecimiento llegan del esfuerzo continuo',
'Acepta las derrotas como las grandes maestras que son. Levántate e intenta de nuevo',
'Cree que lo puedes hacer y lo harás',
'Avanzar, conseguir lo que te propones supone esfuerzo, entrenamiento, sufrimiento. Todo está en nuestras manos…Un nuevo día, un nuevo reto.',
'No esperes conseguir lo más fácil, espera ser el más fuerte.',
'El dolor es temporal, pero tu realización personal es para siempre.',
'Dijeron que no serías capaz, pero aquí estás en el Reto Seiken dándole con todo. ¡¡Sigue asi!!',
'Hazlo ahora, porque a veces mañana se convierte en nunca.',
'Para conseguir el cuerpo que deseas y que nunca tuviste, tienes que hacer aquello que previamente no estuviste dispuesto a hacer.',
'¡Eres más fuerte de lo que crees!',
'El avance podrá ser lento, pero mientras estés ahí, sin duda eres un/una CAMPEÓN/A.',
'Lo que hoy parece imposible, en un futuro será tu calentamiento.',
'Sé más fuerte que tus excusas.'
]

tips_alimentacion = [ 

"La proteina es el macronutriente encargado de construir músculo. En todas tus comidas, que la mitad de tu plato siempre sea proteína.",
"Toma 2-3 litros de agua al día para calmar los antojos.",
"Evita comer alimentos procesados. Siempre prioriza las comidas de un solo ingrediente como el pollo, la papa, el camote, la carne, etc.",
"Para bajar de peso debes estar en un déficit de calorías. Es decir, consumir menos calorías de las que tu cuerpo quema en un día",
"1 pechuga de pollo de 100 gramos tiene 31 gramos de proteina. Con 4 pechugas grandes alcanzarás tus niveles diarios de proteína",
"La Organizacion Mundial de Salud (OMS) recomienda no consumir más de 25 gramos de azúcar al día",
"Todas las células del cuerpo necesitan de agua para funcionar, por eso es esencial ingerir suficiente. Lo ideal es que consumas 2,7 litros de agua potable al día si eres mujer y 3,7 si eres hombre.",
"La OMS recomienda comer 400 gramos diarios de frutas y verduras frescas. Ellas te proporcionan fibra, minerales y vitaminas esenciales para el funcionamiento de todos los órganos",
"En los períodos de ayuno procura ocuparte para evitar pensar en la comida, trata de hacer alguna tarea productiva o ver una interesante película.",
"Bebe agua en abundancia y bebidas sin calorías. En los ayunos es necesario contar con suficiente líquido para conservar el buen ánimo y una buena salud.",
"Si vas a comenzar con el ayuno, comienza por periodos cortos. Esto es lo mejor, y tal vez gradualmente aumentarlos hasta conseguir la adaptación. Recuerda que el cuerpo necesita acoplarse a esta forma de alimentación.",
"No te obsesiones con tu peso. Este puede variar muy facilmente. Si estás viendo cambios en el espejo es porque vas bien.",
"Un buen plan de alimentación debe ser equilibrado y acorde con tu estilo de vida y tus actividades. Evita la monotonía en tu dieta e incluye todos los grupos de alimentos. Cuida, eso sí, las proporciones y las cantidades.",
"Aprende a diferenciar el hambre fisiológico del hambre emocional. El hambre emocional surge cuando estamos ansiosos o aburridos. La puedes reconocer facilmente: si solo te provoca comer un alimento específico, es hambre emocional.",
"Si tienes tendencia a comer entre comidas, opta por tomar una pieza de fruta, un batido de proteína, un té o un café.",
"Si no cocinan mucha proteína en tu casa, hazte 4 huevos duros o hervidos",
"No olvides beber agua en abundancia. A menudo se confunde el hambre con la deshidratación.",
"Evita las bebidas azucaradas, ya que contienen muchas calorías que no le aportan nada a tu cuerpo. Si vas a tomar gaseosa, procura que sea light o zero.",
"Si deseas darte algún capricho ocasional, come una porción pequeña para saciar las ganas. Si el antojo persiste, ingiere una pieza de fruta.",
"1 huevo grande tiene aproximadamente 13 gramos de proteína.",
"Utiliza aceite en spray 0 calorías para cocinar tus comidas",
"El aceite de oliva es saludable pero tiene 884 calorias por 100 gramos. Consúmelo moderadamente"]



mensaje_motivacion=" "
mensaje_alimentacion=" "
contador_pasos=0

logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s,")
logger = logging.getLogger()


TOKEN = os.getenv("5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0")


def start(update: Update, context: CallbackContext):
  name = update.effective_user['first_name']
  update.message.reply_text(f"Hola {name} 👋  Soy tu acompañante virtual 🤖 de SEIKEN y estoy aquí para ayudarte")
  update.message.reply_text(main_menu_message(),
                         reply_markup=main_menu_keyboard())



def echo(update: Update, context: CallbackContext):
    user_id=update.effective_user['id']
    name = update.effective_user['first_name']
    text = update.message.text
    
    context.bot.sendMessage(
        chat_id=user_id,
        parse_mode = "MarkdownV2",
        text = f"Hola, cómo estás __{name}__"
    )


def main_menu(bot, update: Update):
  bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def first_menu(bot, update: Update):
  bot.callback_query.message.edit_text(first_menu_message(),
                          reply_markup=first_menu_keyboard())

def second_menu(bot, update: Update):
  bot.callback_query.message.edit_text(second_menu_message(),
                          reply_markup=second_menu_keyboard())

def third_menu(bot, update: Update):
  bot.callback_query.message.edit_text(third_menu_message(),
                          reply_markup=third_menu_keyboard())



def second_submenu(bot, update: Update):
  pass


def error(update, context: CallbackContext):
    print(f'Update {update} caused error {context.error}')

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Menu 1', callback_data='m1')],
              [InlineKeyboardButton('Menu 2', callback_data='m2')],
              [InlineKeyboardButton('Menu 3', callback_data='m3')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 1-1', callback_data='m1_1')],
              [InlineKeyboardButton('Submenu 1-2', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 2-1', callback_data='m2_1')],
              [InlineKeyboardButton('Submenu 2-2', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)


def third_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Submenu 3-1', callback_data='m3_1')],
              [InlineKeyboardButton('Submenu 3-2', callback_data='m3_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)


############################# Messages #########################################
def main_menu_message():
  return f"Por favor dime, ¿en qué te puedo ayudar? 👀 \n \nEscribe el número de la opción que quieras 👇🏻"

def first_menu_message():
  return 'Choose the submenu in first menu:'

def second_menu_message():
  return 'Choose the submenu in second menu:'


def third_menu_message():
  return 'Choose the submenu in third menu:'






###########

def envio_motivacion_mañana():
    global mensaje_motivacion
    mensaje_elegido = random.choice(mensajes__motivacion_mañana)

    while mensaje_elegido == mensaje_motivacion:
        mensaje_elegido = random.choice(mensaje_elegido)

    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(f"{random.choice(mensajes__motivacion_mañana)}")
    requests.get(base_url)
    
def envio_tips_alimentacion():
    global mensaje_alimentacion
    mensaje_elegido = random.choice(tips_alimentacion)
    while mensaje_elegido == mensaje_alimentacion:
        mensaje_elegido = random.choice(tips_alimentacion)
        
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(mensaje_elegido)
    mensaje_alimentacion=mensaje_elegido
    requests.get(base_url) 

def envio_chequeo_quincenal():
    ## Extraer los correos de los inscritos y mandares un email 
    chequeo_quincenal = '🚨 IMPORTANTE 🚨' + '\n' + 'Hoy es día de CHEQUEO. Sube tu progreso aquí' + '\n' + '👉🏻 https://forms.gle/ZCotB7TLspT8f1vQ7 👈🏻'
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format((chequeo_quincenal))
    requests.get(base_url) 

def envio_pasos_diarios(): ## cómo hacer para que se envíe un elemento de la lista a la vez
    global contador_pasos
    pasos_diarios = [ ]

    for j in range(1000,20000,320):
        pasos_diarios.append(j)

    pasos_diarios.pop()
    pasos_diarios.append(20000)
    base_url = 'http://api.telegram.org/bot5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0/sendMessage?chat_id=-1001621138106&text="{}"'.format(((f"El objetivo de pasos de hoy es: 🔥 {[pasos_diarios[contador_pasos]]}🔥 ")))
    requests.get(base_url)
    contador_pasos = contador_pasos + 1
        
def mensajes_bienvenida(update,context):
    bot=context.bot
    chatID=update.message.chat_id
    print(chatID)
    updateMsg= getattr(update,"message",None)
    for user in updateMsg.new_chat_members:
        username=user.first_name

    logger.info(f'El usuario {username} ha ingresado al grupo')

    mensajes_bienvenida = [ f'Bienvenido al Reto Seiken 2022, {username}. Vamos a darle con todo bro 💪🏻🔥', 
    f'Hola {username}, bienvenido', 
    f'¡{username}! Bienvenido bro, un gusto que estés aquí',
    f'Hola {username}, bienvenido al Reto Seiken 2022, estamos seguros de que podrás tener los cambios que estás buscando. A darle',
    f'Bienvenido a la comunidad Seiken {username}',
    f'Hola {username}, bienvenido. Estamos aquí para lo que necesites']

    bot.sendMessage(
        chat_id=chatID,
        parse_mode="HTML",
        text= random.choice(mensajes_bienvenida)
    )
# def start(update,context):
#     context.job_queue.run_repeating(envio_tips_alimentacion, interval=10, first=10,context=update.message.chat_id)


scheduler1 = BackgroundScheduler()
scheduler2 = BackgroundScheduler()
scheduler3 = BackgroundScheduler()
scheduler4 = BackgroundScheduler()


### MAIN ### 

if __name__== "__main__":
    my_bot = telegram.Bot(token="5009969397:AAFOwZGAFmlHkLL2fnVAqM5pQjUynZ7rAe0")
    #scheduler1.add_job(envio_tips_alimentacion, 'interval', hours=24, start_date='2022-01-20 21:55:00', end_date='2022-02-20 21:55:00')
    # scheduler1.add_job(id='Scheduled task', func=envio_tips_alimentacion, trigger='interval', seconds=5)
    print(my_bot.getMe())
    scheduler1.add_job(envio_tips_alimentacion, 'interval', hours=24, start_date='2022-01-21 12:15:00', end_date='2022-02-20 21:55:00')
    scheduler1.start()
    scheduler2.add_job(envio_motivacion_mañana, 'interval', hours=0.5, start_date='2022-01-21 12:11:00', end_date='2022-02-20 21:55:00')
    scheduler2.start()
    scheduler3.add_job(envio_chequeo_quincenal, 'interval', hours=0.5, start_date='2022-01-21 12:12:00', end_date='2022-02-20 21:55:00')
    scheduler3.start()
    scheduler4.add_job(envio_pasos_diarios, 'interval', hours=0.5, start_date='2022-01-21 12:13:00', end_date='2022-02-20 21:55:00')
    scheduler4.start()


updater=Updater(my_bot.token, use_context=True)



#Creando un despachador
dp=updater.dispatcher

#Creando los manejadores
# dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("start",start))
dp.add_handler(MessageHandler(Filters.text, echo))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,mensajes_bienvenida))
updater.dispatcher.add_error_handler(error)



#### MENUS #####
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
updater.dispatcher.add_handler(CallbackQueryHandler(third_menu, pattern='m3'))


updater.dispatcher.add_handler(CallbackQueryHandler(first_submenu, pattern='m1_1'))
updater.dispatcher.add_handler(CallbackQueryHandler(second_submenu, pattern='m2_1'))


updater.start_polling()
print("BOT LISTO")
updater.idle()


