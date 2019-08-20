import telebot
from telebot import types
from webscript import WebParser
bot = telebot.TeleBot("957915230:AAGNCcR-iZvs1hvYcZFoyhEBAVkZ8dN5ZFM")

colour = 0
name = ""
k = 0

@bot.message_handler(content_types=['text'])
def start(message):
    global k
    k = 0
    if message.text == '/start':
        str1 = "Вы выбираете играть за ястреба (Я) или курицу (К)."
        bot.send_message(message.from_user.id, str1)
        bot.send_message(message.from_user.id, "Отправь твой номер счета в ЛЭШ (только число)")
        bot.register_next_step_handler(message, get_money)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')



def get_money(message):
    global name
    try:
        name = int(message.text)
        keyboard = types.InlineKeyboardMarkup()
        key_blue = types.InlineKeyboardButton(text='ястреб', callback_data='hawk')
        keyboard.add(key_blue)
        key_orange= types.InlineKeyboardButton(text='курица', callback_data='chicken')
        keyboard.add(key_orange)
        question = "Выбери стратегию"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    except Exception:
        bot.send_message(message.from_user.id, "Не ври, такого числа нет. Начинай сначала!")


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global colour
    global k
    if call.data == "hawk" and k == 0:
        colour = "hawk"
        k+=1
        bot.send_message(call.message.chat.id, 'Вы выбрали стратегию ястреба. Ваш ответ записан, спасибо за участие!')
        f = open('predators.txt', 'a')
        wr = str(name)
        f.write(wr + '\n')
        f.close()
        ses = WebParser.authentication(logs=True)
        WebParser.upload_file(session=ses, path="lsh-bot/", file="predators.txt")
        
    elif call.data == "chicken" and k == 0:
        bot.send_message(call.message.chat.id, 'Стратегия "курица" успешно выбрана. Участвуйте снова завтра!')
        k += 1
        f = open('chicks.txt', 'a')
        wr = str(name)
        f.write(wr + '\n')
        f.close()
        ses = WebParser.authentication(logs=True)
        WebParser.upload_file(session=ses, path="lsh-bot/", file="chicks.txt")
        
    elif k >= 1:
        bot.send_message(call.message.chat.id, "Много тыкаешь, начинай сначала. /start ?")


bot.polling(none_stop=True, interval=0)
