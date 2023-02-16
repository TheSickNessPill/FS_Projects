import json
import telebot

from extentions import CryptoConverter, ConvertionException


with open("main_config.txt", mode="r") as file:
    CONFIG = json.loads(file.read())

bot = telebot.TeleBot(CONFIG["tel_token"])
print(bot)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    help_text = "\
{0}, чтобы узнать сколько Евро в 1м Долларе Сша, \
Вам требуется знать код валют, которыми Вы интересуетесь \
(их можно уточнить командой </values>)\
(если вам нужно узнать код крипто валюты - </values_crypto>).\n\
Ниже представлен пример работы с ботом.\n\
Отправьте боту сообщение в виде:\n\
<код валюты, интересующая>\n\
<код валюты, в которую нужно конвертировать>\n\
<количество интересующей валюты>\n\
Пример:\n\
<BIT USD 1> --> сколько долларов в одном биткоине"
    help_text = help_text.format(message.chat.username)
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=["values"])
def handle_values(message):
    currencys = CryptoConverter().get_currency_file()
    responce_string = "\n".join(
        f"{n + 1} - {k}: {v}" for n, (k, v) in enumerate(currencys.items()) if n < 175
    )
    bot.send_message(message.chat.id, responce_string)

@bot.message_handler(commands=["values_crypto"])
def handle_values(message):
    currencys_crypto = CryptoConverter().get_crypto_currency_file()
    responce_string = "\n".join(
        f"{n + 1} - {k}: {v}" for n, (k, v) in enumerate(currencys_crypto.items())
    )
    bot.send_message(message.chat.id, responce_string)


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['text'])
def handle_convert_text(message):
    try:
        responce = CryptoConverter().convert_currencys(
            message,
            CONFIG["currency_token"]
        )
        bot.send_message(message.chat.id, responce)
    except ConvertionException as e:
        bot.send_message(
            message.chat.id, 
            f"Ошибка пользователя:\n{e}"
        )
    except Exception as e:
        bot.send_message(
            message.chat.id, 
            f"Ошибка обработки команды:\n{e}"
        )

bot.polling(none_stop=True)