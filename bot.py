from config import bot
from words import words
from rasp import rasp
import datetime, time
import requests
from timeit import Timer

todays_date = datetime.date.today().weekday()



@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 
    """ Напиши /rasp для того чтобы узнать расписание на сегодня
        или /covid чтобы узнать текущую статистику короны по выбранной стране""")




@bot.message_handler(commands=['covid'])
def send_covid(message):
    
    global a, c, t, g
    t = time.time()
    mess = "{}, Введите название страны латиницей. Если передумали напишите <strong><em>stop</em></strong>".format(message.from_user.first_name)
    a = message.from_user.id
    g = message
    #c = message.from_user.first_name
    bot.register_next_step_handler(bot.reply_to(message, mess, parse_mode='HTML'), check)


    
def checkAgain(message):
    
    bot.register_next_step_handler(message, check)

def check(message):
    b = message.from_user.id
    if t + 15 < time.time():
        bot.reply_to(g, 'Время вышло')
        bot.send_message(message, 'Можете попробовать снова')
    elif a==b:
        send_covid1(message)
    else:
        #bot.reply_to(message, 'Я отвечаю на команду{}.'.format(c))
        checkAgain(message)

def send_covid1(message):
    
    try:
        if message.text == "all":
            url = ('https://coronavirus-19-api.herokuapp.com/all')
        else:
            url = ('https://coronavirus-19-api.herokuapp.com/countries/{}').format(message.text)
            response = requests.get(url, headers={'Accept':'application/json'})
        data = response.json()
        total = str(data['cases'])
        dead = str(data['deaths'])
        recovered = str(data['recovered'])
        covid_info = ("На сегоднящний день в {}: " + "\n" + "Общее кол-во зараженных: {} " + "\n" + "Умерших: {} " + "\n" + "Выздоровели: {} ").format(message.text, total, dead, recovered)
        bot.reply_to(message, covid_info)
    except:
        bot.reply_to(message, 'Название страны введено не правильно. Повторите попытку заного')         
   
@bot.message_handler(commands=['rasp'])
def send_rasp(message):
    bot.reply_to(message, rasp[todays_date][0])
        
@bot.message_handler(content_types=['text'])
def send_text(message):
    
    m = message.text.lower()
    for word in words:
        if word in m:
            bot.reply_to(message, 'Не матерись!!!')  
            bot.delete_message(message.chat.id, message.message_id)
#bot.polling(none_stop = True)
bot.infinity_polling()

