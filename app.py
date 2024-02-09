import telebot
from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message:telebot.types.Message):
    text = ('Чтобы начать работу, введите команду боту в следующем формате:\n'
'<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.\n'
'Пожалуйта, введите валюты в единственном числе. Если нужна помощь, введите команду /help.\n'
'Посмотреть список всех доступных валют: /values')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неправильное колличество параметров. Пожалуйста, введите только 3 параметра')

        quote, base, amount = values
        total_base = CurrencyConverter.convert(quote.lower(), base.lower(), amount.lower())
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду{e}.')
    else:
        text = f'Цена {amount} {quote.lower()} в {base.lower()} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)