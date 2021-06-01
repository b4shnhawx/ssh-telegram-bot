"""
Telegram bot programmed by b4shnhawx.

https://github.com/b4shnhawx/ssh-telegram-bot

1. Install the dependencies.
2. Obtain the user id by running the /test command. The user id will be displayed in the terminal where the bot is running.
3. Enter the API token and your user id (my_chat_id) in the script.
4. Feel free to add or remove commands or functions.
5. Run the bot!

Note that bots are open to the internet, so any user can start it with their user.
This bot always compares your user id (my_chat_id) with the user id of the user trying to execute critical commands. If the IDs do not match, it will ignore the commands and warn you that someone has tried to execute a command.
Commands are exempt from ID checking:
  - /start
  - /test

Dependencies:
pip3 install telebot
pip3 install python-telegram-bot
"""

from telebot import TeleBot
import telegram
import subprocess
import sys
import time
import os


app = TeleBot(__name__)

### -----------------------------------------------
### -------- Minimal functions for SSH bot --------
### -----------------------------------------------

### --- VARIABLES ---

token = "1740512324:AAEoYe4DGFPPg_cEc69cBbR5gr0opTUNWGM"
my_chat_id = "413496441"
terminal = "inactive"

### --- FUNCTIONS ---

###  START

@app.route('/start')
def start(message):
	chat_id = message['chat']['id']

	if chat_id == int(my_chat_id):
		
		app.send_message(chat_id, "Bot iniciado")
		app.send_message(chat_id, "Comandos disponibles (/help): \n" +
							"/start \n" +
							"/test \n" +
							"/ping_pc \n" +
							"/magic_packet \n" +
							"/cmd bash command \n" +
							"/terminal \n")

	else:
		app.send_message(chat_id, "Parece que no tienes permiso para acceder :(")
		app.send_message(chat_id, "Si realmente quieres usar este bot sigue las instrucciones de mi GitHub para configurarlo por ti mism@:" + 
						"\n\n" +
						"https://github.com/b4shnhawx/ssh-telegram-bot")

		#Send info about intrusion
		app.send_message(my_chat_id, "Alguien ha intentado iniciar sesion en el bot")
    #Send info about the user. Also try to catch the username and if not, will be excepted.
		try:
			app.send_message(my_chat_id, "Name: {} \nUsername: {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['username'], message['from']['id'], message['from']['language_code'], message['text']))
		except:
			app.send_message(my_chat_id, "Name: {} {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['last_name'], message['from']['id'], message['from']['language_code'], message['text']))
      
###  HELP

@app.route('/help')
def test_chat_id(message):
	chat_id = message['chat']['id']

	app.send_message(chat_id, "Comandos disponibles (/help): \n" +
							"/start \n" +
							"/test \n" +
							"/ping_pc \n" +
							"/magic_packet \n" +
							"/cmd bash command \n" +
							"/terminal \n")

###  TEST

@app.route('/test')
def test_chat_id(message):
	chat_id = message['chat']['id']

	print("\n-----------\nBot info: {}\n".format(bot.get_me()))

	try:
		print("Name: {} \nUsername: {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['username'], message['from']['id'], message['from']['language_code'], message['text']))
	except:
		print("Name: {} {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['last_name'], message['from']['id'], message['from']['language_code'], message['text']))
   
	print("Message raw: \n{}".format(message))

###  TERMINAL SWITCH

@app.route('/terminal')
def terminal_mode_selector(message):
	chat_id = message['chat']['id']

	global terminal

	if chat_id == int(my_chat_id) and terminal == "inactive":
		terminal = "active"

		app.send_message(my_chat_id, "Modo terminal: {}".format(terminal))

	elif chat_id == int(my_chat_id) and terminal == "active":
		terminal = "inactive"

		app.send_message(my_chat_id, "Modo terminal: {}".format(terminal))

	else:
		app.send_message(my_chat_id, "Alguien ha intentado EJECUTAR un comando")
		app.send_message(my_chat_id, "Name: {} \nUsername: {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['username'], message['from']['id'], message['from']['language_code'], message['text'])) 
		app.send_message(chat_id, "NI. SE. TE. OCURRA. -.-")

###  CAPTURE ALL TEXT/COMMANDS

@app.route('(?!/).+')
def terminal_mode(message):
	chat_id = message['chat']['id']
		
	if chat_id == int(my_chat_id) and terminal == "active":
		cmd = message['text']
		msg = subprocess.run(
			['bash'], input=cmd, capture_output=True, text=True
		)

		app.send_message(my_chat_id, msg.stdout)
		app.send_message(my_chat_id, msg.stderr)

	elif chat_id == int(my_chat_id) and terminal == "inactive":
		message = "{} :)".format(message['text'])
		app.send_message(my_chat_id, message)

	else:
		app.send_message(my_chat_id, "Alguien ha intentado EJECUTAR un comando")
		app.send_message(chat_id, "NI. SE. TE. OCURRA. -.-")


### ------------------------------------------------
### -------- Optional functions for the bot --------
### ------------------------------------------------

### --- VARIABLES ---

mac_magic_packet = "00:D8:61:BF:60:02"
ip_pc_ping = "192.168.1.10"

### --- FUNCTIONS ---

###  PING

@app.route('/ping_pc')
def ping_pc(message):
	chat_id = message['chat']['id']

	if chat_id == int(my_chat_id):
		msg = subprocess.run(
		  ["ping", "-c5", ip_pc_ping], capture_output=True, text=True
		)
	
		app.send_message(my_chat_id, msg.stdout)
		app.send_message(my_chat_id, msg.stderr)

	else:
		app.send_message(chat_id, "Que no tienes permisos >:(")

###  WAKE ON LAN

@app.route('/magic_packet')
def magic_packet(message):
	chat_id = message['chat']['id']

	if chat_id == int(my_chat_id):
		msg = subprocess.run(
			["wakeonlan", mac_magic_packet], capture_output=True, text=True
		)

		app.send_message(my_chat_id, msg.stdout)
		app.send_message(my_chat_id, msg.stderr)

	else:
		app.send_message(chat_id, "En serio...?")

###  SINGLE COMMAND

@app.route('/cmd ?(.*)')
def cmd(message, cmd):
	chat_id = message['chat']['id']

	if chat_id == int(my_chat_id):
		msg = subprocess.run(
			['bash'], input=cmd, capture_output=True, text=True
		)

		app.send_message(my_chat_id, msg.stdout)
		app.send_message(my_chat_id, msg.stderr)

	else:
		app.send_message(my_chat_id, "Alguien ha intentado EJECUTAR un comando")
		app.send_message(my_chat_id, "Name: {} \nUsername: {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['username'], message['from']['id'], message['from']['language_code'], message['text'])) 
		app.send_message(chat_id, "NI. SE. TE. OCURRA. -.-")

###  EXAMPLE COMMAND

#@app.route('/command_neme')
#def ping_pc(message):
#	chat_id = message['chat']['id']
#
#	if chat_id == int(my_chat_id):
#		msg = subprocess.run(
#		  ["COMMAND", "ARG1", "ARG2", "ARG3", "etc"], capture_output=True, text=True
#		)
#	
#		app.send_message(my_chat_id, msg.stdout)
#		app.send_message(my_chat_id, msg.stderr)
#
#	else:
#		app.send_message(chat_id, "Que no tienes permisos >:(")

### --------------------- MAIN ---------------------
if __name__ == '__main__':
	bot = telegram.Bot(token = token)
	app.config['api_key'] = token
	app.poll(debug=True)