# Telegram

# TELEGRAM
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized



# ACCESO A DATOS EN SERVIDORES (usado por telegram)
#import json 
import requests


import config
import httpUtils
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES TELEGRAM
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm

v = '1.1'

chat_ids = {}

#URL de la API de TELEGRAM
URL = "https://api.telegram.org/bot{}/".format(config.TELEGRAM_API_TOKEN)

def getUsersInfo():
    global chat_ids
    sUsers = 'Users\n===========\n'
    for item in chat_ids:
        sUsers += str(item) + '@'
        sUsers += str(chat_ids[item][0])+' in '
        sUsers += str(chat_ids[item][1])+'\n'
    return sUsers

def send_picture(picture,chat_it):
    global URL
    url = URL+"sendPhoto"
    files = {'photo': open(picture, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

def send_document(doc,chat_it):
    global URL
    url = URL+"sendDocument"
    files = {'document': open(doc, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def send_message(text,chat_id):
    '''
    Funcion para enviar telegramas atraves de la API
    '''
    global URL
    try:
		
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        #print("url >> ",url)
        httpUtils.get_url(url)
    except Exception as e:
        print("ERROR de envio: "+str(e))

