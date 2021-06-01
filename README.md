# SSH Telegram Bot

This bot allows you to execute commands on the system without having to have an SSH connection to the system. As it works with the Telegram API, we don't need to know the public IP of the network or redirect connections via ports.

Personally, I don't think that this bot can completely replace SSH (or any other protocol with which to execute commands on the system) if it is used on a regular basis. The reason why I created this bot is mainly to be able to send some quick commands or to do some basic trouble shooting in case I have no connection to the system, either because I have "broken" something (xD) or because the IP of my DNS domain has changed and I have no connection to my network.

Keep in mind that Telegram bots are public on the internet and any user searching for your bot's name will be able to start it. Since this is a HUGE security issue, I have configured the bot to compare your user ID with the sender's at all times. If the ID matches it means that you are the one trying to execute commands and it will go ahead, but if the ID doesn't match it means that someone other than you is trying to access and execute commands. In this second case the bot will ignore the command, send a message to the impostor and warn you that someone has tried to execute commands, along with the user information.

### - Enable "Telegram SSH"
![Command example](https://github.com/b4shnhawx/ssh-telegram-bot/blob/main/images/command.jpg)
