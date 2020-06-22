# Telegram

# TELEGRAM
import telegram
from telegram import ReplyKeyboardMarkup
from telegram.error import NetworkError, Unauthorized



# ACCESO A DATOS EN SERVIDORES (usado por telegram)
import json 
import requests


import config
import emailUtil
import Datos
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm
# FUNCIONES TELERAM
# mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm



#URL de la API de TELEGRAM
URL = "https://api.telegram.org/bot{}/".format(config.TOKEN)

chat_id = 0

update_id = None

user_keyboard = [['/info','/fig'],['/email', '/txt'],['/save','/ayuda'],['/deleteOld','/deleteNew']]
user_keyboard_markup = ReplyKeyboardMarkup(user_keyboard, one_time_keyboard=True)

""" poner en marcha el bot """
telegram_bot_experimento_bio = telegram.Bot(config.TOKEN)

#comandos a mostrar al pedir '/ayuda'
listaComandos = ["/ayuda - Mostrar esta Ayuda", \
                 "/email - envia datos completos por email",\
                 "/info - Mostrar datos actuales", \
                 "/txt - envia datos completos a telegram", \
                 "/fig - Grafico de Evolucion",\
                 "/deleteOld - Borra los 15 primeros datos",\
                 "/deleteNew - Borra los 15 ultimos datos",\
                 "/save - Realiza una copia de seguridad","\n"]



FLAG_enviar_PNG = False             #controla el proceso de envio de grafica al usuario
FLAG_enviar_TXT = False             #controla el proceso de envio de fichero de datos al usuario

FLAG_delete_old = False           #control de borrado de los primeros datos tomados
FLAG_delete_new = False             #control de borrado de los ultimos datos tomados

FLAG_pruebas = False                #Para hacer pruebas con telegram (sin uso)
FLAG_enviar_INFO = False
FLAG_save_DATA = False
FLAG_send_DATA = False

#bucle para generar el texto encadenando todos los comandos de ayuda.
#Para el mensaje que se envia por telegram al pedir '/ayuda'
listaComandosTxt = ""
for comando in listaComandos:
    listaComandosTxt += comando+"\n"



def get_url(url):
    '''
    Funcion de apoyo a la recogida de telegramas,
    Recoge el contenido desde la url de telegram
    '''
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def send_picture(picture):
    url = URL+"sendPhoto";
    files = {'photo': open(picture, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

def send_document(doc):
    url = URL+"sendDocument";
    files = {'document': open(doc, 'rb')}
    data = {'chat_id' : chat_id}
    r= requests.post(url, files=files, data=data)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def send_message(text):
    '''
    Funcion para enviar telergamas atraves de la API
    '''
    try:
        url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        #print("url >> ",url)
        get_url(url)
    except:
        print("ERROR de envio")

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------  

def atenderTelegramas():
    '''
    Funcion principal de la gestion de telegramas.
    Los atiende y procesa, ejecutando aquellos que son ordenes directas.
    Solicita la 'ayuda' de otras funciones para aquellos comandos
    complejos que contiene parametros
    '''
    global text, chat_id, chat_time, comando, chat_user_name
    global FLAG_enviar_PNG, FLAG_pruebas, FLAG_enviar_TXT, FLAG_delete_old, FLAG_delete_new, FLAG_enviar_INFO,FLAG_save_DATA,FLAG_send_DATA

    global update_id
    
    try:    
        # Request updates after the last update_id
        for update in telegram_bot_experimento_bio.get_updates(offset=update_id, timeout=0): #timeout=5, si nos da problemas con internet lento
            update_id = update.update_id +1

            if update.message:  # porque se podrian recibir updates sin mensaje...
                comando = update.message.text  #MENSAJE_RECIBIDO
                chat_time = update.message.date
                user = update.message.from_user #USER_FULL
                chat_id = int(update.message.from_user.id)
                chat_user_name = user.first_name #USER_REAL_NAME
                usuario = chat_user_name
                            
                try:
                    # para DEBUG, imprimimos lo que va llegando
                    print (str(chat_time) + " >>> " + str(chat_id) +": " + usuario + " --> " + comando)
                    
                    if update.message.entities[0].type == "bot_command" and update.message.text == "/start":
                        update.message.reply_text("Bienvenido a Experimento Bio v1.1", reply_markup=user_keyboard_markup)
                                            
                    # ===============   INTERPRETAR LOS COMANDOS QUE LLEGAN Y ACTUAR EN CONSECUENCIA   ===============
                    
                    if comando == "/send" and (chat_id == config.ADMIN_USER or config.ADMIN_USER == None):  #decidir quien puede enviar correos
                        FLAG_send_DATA = True
                        return
          
                    if comando == "/save" and (chat_id == config.ADMIN_USER or config.ADMIN_USER == None):  #solo el administrador puede forzar el salvado de datos no programado
                        FLAG_save_DATA = True
                        return

                    # Lista de comandos para usuarios basicos (clientes)           
                    if comando == "/ayuda":
                        send_message (listaComandosTxt)
                        return
                    
                    if comando == "/info":
                        FLAG_enviar_INFO = True
                        return

                    if comando == "/fig":
                        FLAG_enviar_PNG = True
                        return 
                    
                    if comando == "/txt":
                        FLAG_enviar_TXT = True
                        return
                     
                    if comando == "/deleteOld" and (chat_id == config.ADMIN_USER or config.ADMIN_USER == None):
                        FLAG_delete_old = True
                        return
                    
                    if comando == "/deleteNew" and (chat_id == config.ADMIN_USER or config.ADMIN_USER == None):
                        FLAG_delete_new = True
                        return
                except:
                    print ("----- ERROR ATENDIENDO TELEGRAMAS ----------------------")                      
                if chat_id != 0:
                    #ante cualquier comando desconocido devolvemos 'ok', para despistar a los que intenten 'probar suerte'
                    send_message ("OK")  
        
    except:
        pass
    
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
    