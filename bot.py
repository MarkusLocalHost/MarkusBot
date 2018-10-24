import telebot
import psycopg2
from telebot import types
import flask



bot = telebot.TeleBot(token)

#server
server = flask.Flask(__name__)



# database connection
conn_string = "host='localhost' dbname='geo_data' user='markus' password='98712304q'"
print("Connecting to database\n	->%s" % (conn_string))
conn = psycopg2.connect(conn_string)
cur = conn.cursor()


# start message
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembot_1 = types.KeyboardButton('Банкоматы')
    itembot_2 = types.KeyboardButton('Кафе')
    itembot_3 = types.KeyboardButton('Рестораны')
    keyboard.add(itembot_1, itembot_2, itembot_3)
    bot.send_message(message.chat.id, "Привет, я умею искать ближайшие к тебе объекты, выбери из списка что тебе нужно",
                     reply_markup=keyboard)

# location from users
@bot.message_handler(content_types=['location'])
def handle_location(message):
    lat = message.location.latitude
    long = message.location.longitude
    bot.send_message(message.chat.id, text="Я запомнил твое местопложение, можно начинать")
    print(lat, long)


# Work with bank
@bot.message_handler(func=lambda mess: "Банкоматы" == mess.text, content_types=['text'])
def handle_bank(message):
    keyboard_bank = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Сбербанк", callback_data="bank-sberbank")
    callback_button2 = types.InlineKeyboardButton(text="Альфа-банк", callback_data="bank-alpha")
    keyboard_bank.add(callback_button1, callback_button2)
    bot.send_message(message.chat.id, "Ты выбрал банкоматы, теперь необходимо выбрать банкомат какого банка тебе нужен",
                     reply_markup=keyboard_bank)


# Work with cafe
@bot.message_handler(func=lambda mess: "Кафе" == mess.text, content_types=['text'])
def handle_cafe(message):
    keyboard_cafe = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="<1000р", callback_data="check<1000")
    callback_button2 = types.InlineKeyboardButton(text="<1000-1500>", callback_data="check>1000")
    callback_button3 = types.InlineKeyboardButton(text="<1500-2000>", callback_data="check>1500")
    callback_button4 = types.InlineKeyboardButton(text="<2000-3000>", callback_data="check>2000")
    keyboard_cafe.add(callback_button1, callback_button2, callback_button3, callback_button4)
    bot.send_message(message.chat.id, "Ты выбрал кафе, теперь необходимо выбрать какой средний чек тебя устраивает",
                     reply_markup=keyboard_cafe)


# Work with restaurants
@bot.message_handler(func=lambda mess: "Рестораны" == mess.text, content_types=['text'])
def handle_cafe(message):
    keyboard_rest = types.InlineKeyboardMarkup()
    callback_button1 = types.InlineKeyboardButton(text="Азиаткая кухня", callback_data="kit-asian")
    callback_button2 = types.InlineKeyboardButton(text="Итальянская", callback_data="kit-ital")
    callback_button3 = types.InlineKeyboardButton(text="Французская кухня", callback_data="kit-fran")
    keyboard_rest.add(callback_button1, callback_button2, callback_button3)
    bot.send_message(message.chat.id, "Ты выбрал рестораны, теперь нужно выбрать национальность кухни",
                     reply_markup=keyboard_rest)


# Work with inline call
@bot.callback_query_handler(func=lambda call: True)
def id_callback(query):
    data = query.data
    if data.startswith('bank-'):
        if query.data == 'bank-sberbank':
            cur.execute("SELECT longitude FROM bankomat")
            long_db = cur.fetchall()
            print(long_db)
            cur.execute("SELECT latitude FROM bankomat")
            lat_db = cur.fetchall()
            print(lat_db)
            print(type(lat_db))
            a = float()
            a = float(lat_db[0][0])
            b = float(lat_db[1][0])
            c = float(lat_db[2][0])
            d = float(lat_db[3][0])
            print(a)
            print(type(a))
            print(b)
            print(c)
            print(d)


            # algoritm of search
            for _ in range(4):
                rast = (float(lat_db[0][1]-lat))

            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=f"{a}, {b}")
        elif query.data == 'bank-alpha':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Тут информация о том сколько банкоматов альфы в городе")

    elif data.startswith('check'):
        if query.data == 'check<1000':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Тут информация о чеках <1000")
        elif query.data == 'check>1000':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Тут информация о чеках >1000")
        elif query.data == 'check>1500':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Тут информация о чеках >1500")
        elif query.data == 'check>2000':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="Тут информация о чеках >2000")

    elif data.startswith('kit-'):
        if query.data == 'kit-asian':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  text="Тут информация о ресторанах азиатской кухни")
        elif query.data == 'kit-ital':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  text="Тут информация о ресторанах итальянской кухни")
        elif query.data == 'kit-fran':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id,
                                  text="Тут информация о ресторанах французской кухни")




bot.polling(none_stop=True, timeout=123)