"""
Telegram bot programmed by b4shnhawx.

https://github.com/b4shnhawx/ssh-telegram-bot

1. Install the dependencies.
2. Get the user id by running the /test command. The user id will be displayed in the terminal where the bot is running.
3. Enter the API token and the user id of the user you want to allow (permit_chat_id) in the script.
4. Feel free to add or remove commands or functions.
5. Run the bot!

Note that bots are open to the Internet, so any user can start it with their user.
This bot always compares the ids of the users allowed to use the bot (permit_chat_id) with the id of the user trying to execute critical commands. If the IDs do not match, it will ignore the commands and warn you that someone has tried to execute a command.
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
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

app = TeleBot(__name__)

### -----------------------------------------------
### -------- Minimal functions for SSH bot --------
### -----------------------------------------------

### --- VARIABLES ---

token = "xxxxxxxxx:ABCDEFabcdef..."
permit_chat_id = (CHAT_ID_1, CHAT_ID_2, CHAT_ID_3...)
terminal = "inactive"

### --- FUNCTIONS ---

###  SEND USER INFO

def info_anon_user(permited_user, message):
  #Send info about the user. Also try to catch the username and if not, will be excepted.
	try:
		app.send_message(permited_user, "Name: {} \nUsername: {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['username'], message['from']['id'], message['from']['language_code'], message['text']))
	except:
		#app.send_message(permited_user, "Name: {} {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['last_name'], message['from']['id'], message['from']['language_code'], message['text']))
		app.send_message(permited_user, "Name: {} {} \nChat ID: {} \nText: {}".format(message['from']['first_name'], message['from']['last_name'], message['from']['id'], message['text']))
      
###  START RESTRICTED

@app.route('/start')
def start(message):
	chat_id = message['chat']['id']

	if chat_id in permit_chat_id:
		
		app.send_message(chat_id, "Bot iniciado")
		app.send_message(chat_id, "Comandos disponibles (/help): \n" +
							"/start \n" +
							"/test \n" +
							"/ping_pc \n" +
							"/public_ip \n" +
							"/magic_packet_pc \n" +
							"/suspend_pc MINUTOS\n" +
							"/logoff_pc \n" +
							"/shut_down_pc \n" +
							"/cmd bash command \n" +
							"/terminal \n")

	else:
		app.send_message(chat_id, "Parece que no estas en la whitelist :(")
		app.send_message(chat_id, "Si realmente quieres usar este bot sigue las instrucciones de mi GitHub para configurarlo por ti mism@:" + 
						"\n\n" +
						"https://github.com/b4shnhawx/ssh-telegram-bot")

		for permited_user in permit_chat_id:
			#Send info about intrusion
			app.send_message(permited_user, "Alguien ha intentado iniciar sesion en el bot")
			#Send info about the user
			info_anon_user(permited_user, message)

###  HELP

@app.route('/help')
def test_chat_id(message):
	chat_id = message['chat']['id']

	app.send_message(chat_id, "Comandos disponibles (/help): \n" +
							"/start \n" +
							"/test \n" +
							"/ping_pc \n" +
							"/public_ip \n" +
							"/magic_packet_pc \n" +
							"/suspend_pc \n" +
							"/logoff_pc \n" +
							"/shut_down_pc \n" +
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

	if chat_id in permit_chat_id and terminal == "inactive":
		terminal = "active"

		app.send_message(chat_id, "Modo terminal: {}".format(terminal))

	elif chat_id in permit_chat_id and terminal == "active":
		terminal = "inactive"

		app.send_message(chat_id, "Modo terminal: {}".format(terminal))

	else:
		app.send_message(chat_id, "NI. SE. TE. OCURRA. -.-")

		for permited_user in permit_chat_id:
			#Send info about intrusion
			app.send_message(permited_user, "Alguien ha intentado EJECUTAR un comando en el bot")
			#Send info about the user
			info_anon_user(permited_user, message)

###  CAPTURE ALL TEXT/COMMANDS

@app.route('(?!/).+')
def terminal_mode(message):
	chat_id = message['chat']['id']
		
	if chat_id in permit_chat_id and terminal == "active":
		cmd = message['text']
		msg = subprocess.run(
			['bash'], input=cmd, capture_output=True, text=True
		)

		app.send_message(chat_id, msg.stdout)
		app.send_message(chat_id, msg.stderr)

	elif chat_id in permit_chat_id and terminal == "inactive":
		message = "{} :)".format(message['text'])
		app.send_message(chat_id, message)

	else:
		for permited_user in permit_chat_id:
			app.send_message(permited_user, "Alguien ha escrito algo al bot:")
			info_anon_user(permited_user, message)
   
			message = "{} :)".format(message['text'])
			app.send_message(permited_user, message)
		


### ------------------------------------------------
### -------- Optional functions for the bot --------
### ------------------------------------------------

### --- VARIABLES ---

mac_magic_packet = "00:D8:61:BF:60:02"
ip_pc = "192.168.1.10"
user = "NAS"
password = "WS-dah4909"

### --- FUNCTIONS ---

###  PING

@app.route('/ping_pc')
def ping_pc(message):
	chat_id = message['chat']['id']

	if chat_id in permit_chat_id:
		msg = subprocess.run(
		  ["ping", "-c5", ip_pc], capture_output=True, text=True
		)
	
		app.send_message(chat_id, msg.stdout)
		app.send_message(chat_id, msg.stderr)

	else:
		app.send_message(chat_id, "Que no tienes permisos >:(")

###  PUBLIC IP

@app.route('/public_ip')
def ping_pc(message):
        chat_id = message['chat']['id']

        if chat_id in permit_chat_id:
                msg = subprocess.run(
                  ["curl", "ifconfig.me"], capture_output=True, text=True
                )

                app.send_message(chat_id, msg.stdout)
                app.send_message(chat_id, msg.stderr)

        else:
                app.send_message(chat_id, "Que no tienes permisos >:(")


###  WAKE ON LAN

@app.route('/magic_packet_pc')
def magic_packet_pc(message):
	chat_id = message['chat']['id']

	if chat_id in permit_chat_id:
		msg = subprocess.run(
			["wakeonlan", mac_magic_packet], capture_output=True, text=True
		)

		app.send_message(chat_id, msg.stdout)
		app.send_message(chat_id, msg.stderr)

	else:
		app.send_message(chat_id, "En serio...?")

###  SUSPEND PC VIA SSH

@app.route('/suspend_pc ?(.*)')
def suspend_pc(message, time):
	chat_id = message['chat']['id']

	if time == "":
		msg = "Ingresa el numero de minutos despues del comando para empezar la cuenta atras"

		app.send_message(chat_id, msg)

	elif chat_id in permit_chat_id:

		time_minutes = int(time) * 60
		time_hours = int(time) / 60

		msg = "Suspenso programado para dentro de {} horas".format(time_hours)
		app.send_message(chat_id, msg)

		cmd = 'powershell -command "Start-Sleep -s {}" && powershell -command "%windir%\\System32\\rundll32.exe powrprof.dll,SetSuspendState Hibernate"'.format(time_minutes)
		print(cmd)
		
		ssh.connect(ip_pc, username=user, password=password)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		
		#print(stdout.readlines())

		time.sleep(2)

		

	else:
		app.send_message(chat_id, "En serio...?")

###  LOGOFF SESSION

@app.route('/logoff_pc')
def logoff_pc(message):
	chat_id = message['chat']['id']

	if chat_id in permit_chat_id:

		msg = "Cerrando sesion en el ordenador"
		
		cmd = '%windir%\\System32\\shutdown.exe -l'
		
		ssh.connect(ip_pc, username=user, password=password)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		
		#print(stdout.readlines())

		time.sleep(2)
		ssh.close()

		app.send_message(chat_id, msg)

	else:
		app.send_message(chat_id, "En serio...?")

###  SHUT DOWN PC

@app.route('/shut_down_pc')
def logoff_pc(message):
        chat_id = message['chat']['id']

        if chat_id in permit_chat_id:

                msg = "Apagando el ordenador"

                cmd = 'shutdown/s'

                ssh.connect(ip_pc, username=user, password=password)
                stdin, stdout, stderr = ssh.exec_command(cmd)

                #print(stdout.readlines())

                time.sleep(2)
                ssh.close()

                app.send_message(chat_id, msg)

        else:
                app.send_message(chat_id, "En serio...?")


###  SINGLE COMMAND

@app.route('/cmd ?(.*)')
def cmd(message, cmd):
	chat_id = message['chat']['id']

	if chat_id in permit_chat_id:
		msg = subprocess.run(
			['bash'], input=cmd, capture_output=True, text=True
		)

		app.send_message(chat_id, msg.stdout)
		app.send_message(chat_id, msg.stderr)

	else:
		for permited_user in permit_chat_id:
			app.send_message(permited_user, "Alguien ha intentado EJECUTAR un comando")
			app.send_message(permited_user, "Name: {} \nUsername: {} \nChat ID: {} \nLanguage: {} \nText: {}".format(message['from']['first_name'], message['from']['username'], message['from']['id'], message['from']['language_code'], message['text'])) 
			app.send_message(chat_id, "NI. SE. TE. OCURRA. -.-")

###  EXAMPLE COMMAND

#@app.route('/command_name')
#def ping_pc(message):
#	chat_id = message['chat']['id']
#
#	if chat_id in permit_chat_id:
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
while True:
	if __name__ == '__main__':
		try:
			bot = telegram.Bot(token = token)
			app.config['api_key'] = token
			app.poll(debug=True)
		except:
			#app.send_message(my_chat_id, "Ha ocurrido un error durante la ejecucion del bot")
			pass
