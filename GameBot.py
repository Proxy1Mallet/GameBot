from time import time
from random import randint, choice
from string import punctuation
from telebot import TeleBot
from json import dump, load
from config import *

bot = TeleBot(token)

@bot.message_handler(func = lambda message : True)
def playGame(msg):
    text = msg.text.lower().translate(str.maketrans('', '', punctuation))
    userId = msg.from_user.id
    chatId = msg.chat.id

    send = bot.send_message
    with open(f'{userId}.json') as database: data = load(database)

    if text == 'начать':
        if msg.from_user.last_name is None: name = f"{msg.from_user.first_name}"
        else: name = f"{msg.from_user.first_name} {msg.from_user.last_name}"
        data = {
            "coin": 0,
            "name": name,
            "time": int(time().real)
        }
        send(chatId, startMessage(name))

    if text == 'работа':
        if int(time().real) >= data['time'] + 600:
            randomMoney = randint(0, 100)
            data['coin'] += randomMoney
            data['time'] = int(time().real)
            send(chatId, moneyPlus(data['name'], randomMoney))
        else: send(chatId, notTime(data['name']))

    if text == 'баланс': send(chatId, balans(data['name'], data['coin']))

    if text == 'казино':
        if data['coin'] != 0:
            if randint(1, 5) == 2:
                data["coin"] *= 2
                send(chatId, congratulations(data['name']))
            else:
                data['coin'] = 0
                send(chatId, regrets(data['name']))
        else: send(chatId, noCoins(data['name']))
    with open(f"{userId}.json", "w") as database: dump(data, database)

bot.polling(non_stop = True)