
from start2 import start
import telebot
from telebot import types
import time
import datetime
import sys
try:
    import imaplib2
except ImportError:
    raise SystemExit("Module imaplib2 is required (try <pip3 install ./imaplib2-master).")

if (sys.maxsize <= 2**32):
    raise SystemExit("Program must run on a 64bit system.")


API_TOKEN="951787503:AAE6qHomMQn2wWBFOgqR-rEboUMgTrDtNOY"
bot = telebot.TeleBot(API_TOKEN)
 
def hdl(message):
    instance = start(message,bot)

@bot.message_handler(commands = ["start"])
def welcome(message):
    try:
        sti = open('welcome.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        x = datetime.datetime.now()
        h = x.hour
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Si', 'No')
        if(h<=12):
            r =  bot.send_message(message.chat.id, "Buenos días, bienvenido, ¿desea conectarse a su servicio de correo electrónico?", reply_markup=markup)
        elif(h<=18):
            r =  bot.send_message(message.chat.id, "Buenas tardes, bienvenido, ¿desea conectarse a su servicio de correo electrónico?", reply_markup=markup)
        else:
            r =  bot.send_message(message.chat.id, "Buenas noches, bienvenido, ¿desea conectarse a su servicio de correo electrónico?", reply_markup=markup)
        bot.register_next_step_handler(r, hdl)
       

    except Exception as e:
        bot.send_message(message.chat.id, 'Disculpe')
        sti = open('error.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        print(e)

bot.polling() #no se cierra el programa
