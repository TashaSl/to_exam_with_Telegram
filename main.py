import telebot
import re
import config
from Model import Model

URL = "https://api.telegram.org/bot%s/" % config.BOT_TOKEN

bot = telebot.TeleBot(config.BOT_TOKEN)
db = Model()

@bot.message_handler(commands=['help'])
def help(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, 'Поможет быстро сориентироваться в шпаргалках\n' + 
        '/ номер вопроса - выдаст ответ из шпаргалки\n' +
        'часть вопроса - найдет похожие вопросы\n' +
        '/start - для начала работы\n' +
        '/all - для вывода всего списка вопросов\n' +
        '/author - для связи с разработчиком')

@bot.message_handler(commands=['start'])
def start(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, 'наберите /1')

@bot.message_handler(commands=['all'])
def all_questions(message): # Название функции не играет никакой роли, в принципе
    r = db.get_all_questions()
    for element in separation_big_message(r):
        bot.send_message(message.chat.id, element)

@bot.message_handler(commands=['author'])
def author(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, 'Разработчик: Наталия Соломкина\ntasha@gcor.ru')   

@bot.message_handler(content_types = ['text'])
def different(message): # Название функции не играет никакой роли, в принципе
    if message.text[0] != '/':
        r = db.find_questions(message.text)
        if type(r) != list:
            bot.send_message(message.chat.id, 'такого вопроса не найдено')
        else:
            r = '\n'.join(r)
            bot.send_message(message.chat.id, 'Попробуйте:\n')
            for element in separation_big_message(r):
                bot.send_message(message.chat.id, element)
    else:
        m = message.text.split(' ')[0]
        m = ''.join(re.findall('[0-9]', m))
        if m == '':
            bot.send_message(message.chat.id, 'Что-то пошло не так')
        else:
            r = db.find(int(m) - 1)
            if r == '':
                r = 'Ответ пустой'
            for element in separation_big_message(r):
                bot.send_message(message.chat.id, element)
            

def separation_big_message(message):
    arr = []
    if len(message) > 600:
        i = 0
        while i < len(message):
            arr.append(message[i:i + 600])
            i += 600
    else:
        arr.append(message)
    return arr

if __name__ == '__main__':
     bot.polling(none_stop=True)