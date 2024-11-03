import random
import threading
import time
from program.tokens import mas_tokens
import telebot
from telebot import types
from telebot.types import InputMediaPhoto,InputMediaVideo

from program.DataBase import *

numtime=2
token = mas_tokens[2]#token tg бота
bot = telebot.TeleBot(token)
channel_name=[]
Posts_id = []
SelectPost=[]
id_channel = mas_tokens[3]
time_posts =[]
Chek_mas=[]

@bot.message_handler(commands=['settime'])
def setTime(message):
    prefstart(message)

@bot.message_handler(commands=['start'])
def start(message):
    Chek_mas.clear()
    if(numtime==120):
        bot.send_message(message.chat.id, "Время периода стоит 2 минуту чтобы поменять напишите /settime")
    rT = threading.Thread(target=cycle)
    try:
        rT.join()
    except:
        pass
    rT.start()
    global Posts_id
    Posts_id = []
    bot.send_message(message.chat.id, "Сейчас посмотрим какие посты вы еще не опубликовали")
    db = sqlite3.connect("Media.db")
    Base = DataBaseMedia(db)
    mas = Base.Fetch()
    Base.Close()
    print(mas)

    for i in mas:
        Chek_mas.append(i)
        if(i[3]==0):
            Posts_id.append(i[0])

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Посмотреть есть ли новые посты", callback_data='chek_text_all')
    btn2 = types.InlineKeyboardButton("Посмотреть новые посты", callback_data='chek_new')
    btn3 = types.InlineKeyboardButton("Посмотреть какие посты в очереди", callback_data='chek_queue')
    markup.row(btn1)
    markup.row(btn2)
    markup.row(btn3)
    bot.send_message(message.chat.id, 'Выбирите дальнейшее действие',
                     reply_markup=markup)


@bot.message_handler(commands=['chek_channels'])
def ChekChannels(message):
    if (numtime == 120):
        bot.send_message(message.chat.id, "Время периода стоит 2 минуту чтобы поменять напишите /settime")
    st = PrintName()[1]
    bot.send_message(message.chat.id, "Добавленные каналы:" + st)


@bot.message_handler(commands=['add'])
def Add(message):
    if (numtime == 120):
        bot.send_message(message.chat.id, "Время периода стоит 2 минуту чтобы поменять напишите /settime")
    st = PrintName()[1]
    bot.send_message(message.chat.id, "Добавленные каналы:"+st)
    bot.send_message(message.chat.id, "Напишите мне каналы с колторыми мы будем работать")
    bot.register_next_step_handler(message, ChannelAdd)


@bot.message_handler(commands=['delete'])
def Delete(message):
    if (numtime == 120):
        bot.send_message(message.chat.id, "Время периода стоит 2 минуту чтобы поменять напишите /settime")
    bot.send_message(message.chat.id, "Напишите Название канала для удвления")
    bot.register_next_step_handler(message, DelName)


def ChannelAdd(message):
    if ("/" in message.text):
        bot.send_message(message.chat.id, "Канал не может начинаться с /")
    else:
        if(Chek(message.text)==False):
            db = sqlite3.connect("Media.db")
            Base = DataBaseChannels(db)
            Base.AddIntoDB(message.text)
            Base.Close()
            channel_name.append(message.text)
            markup = types.InlineKeyboardMarkup()
            btn1 = types.InlineKeyboardButton("Добавить еще канал", callback_data='add')
            btn2 = types.InlineKeyboardButton("Я уже все добавил", callback_data='stop')
            markup.add(btn1, btn2)
            bot.send_message(message.chat.id, 'Выбирите дальнейшее действие',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Этот канал уже есть в вашем списке, выбирите другой")
            bot.register_next_step_handler(message, ChannelAdd)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global Posts_id
    global SelectPost
    values = call.data
    if (values == 'add'):
        bot.send_message(call.message.chat.id, "Напишите мне каналы с колторыми мы будем работать")
        bot.register_next_step_handler(call.message, ChannelAdd)

    if(values == 'stop'):

        st =""
        for i in channel_name:
            st+="\n"+" "+i

        bot.send_message(call.message.chat.id, f"Вы добавили каналы:{st}")

    if(values == 'chek_text_all'):
        markup = types.InlineKeyboardMarkup(row_width=3)
        for i in Posts_id:
            btn = types.InlineKeyboardButton("Посмотреть пост - " + str(i), callback_data=i)
            markup.add(btn)
        bot.send_message(call.message.chat.id, 'Выбирите пост для просмотра и редактирования',
                         reply_markup=markup)
    if(values == 'keep'):
        global SelectPost
        print(SelectPost)
        db = sqlite3.connect("Media.db")
        Base = DataBaseMedia(db)
        Base.UpdatePublished(SelectPost[0], 1)
        #mas = Base.Select(SelectPost[0])
        Base.Close()
        bot.send_message(call.message.chat.id, 'Пост добавлен в очередь')




    if(values == 'edit_text'):
        bot.send_message(call.message.chat.id, "Напишите текст чтобы заменить его")
        bot.register_next_step_handler(call.message, EditMessage)

    if(values in list(map(str,Posts_id))):
        db = sqlite3.connect("Media.db")
        Base = DataBaseMedia(db)
        mas = Base.Select(int(values))
        mas = mas[0]
        Base.Close()
        SelectPost = mas
        #EditMessage(mas)
        MediaSendPost([mas[1],mas[4],mas[5],mas[0]], call.message.chat.id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Редактировать текст", callback_data='edit_text')
        btn2 = types.InlineKeyboardButton("Все окей можно добавить в очередь", callback_data='keep')
        markup.row(btn1)
        markup.row(btn2)
        bot.send_message(call.message.chat.id, 'Выбирите дальнейшее действие',
                         reply_markup=markup)

    if(values == "chek_queue"):
            print(Chek_mas)
            for i in Chek_mas:
                if(i[6]==0 and i[3]==1):
                    bot.send_message(call.message.chat.id, f"пост под номером {i[0]}")
                    MediaSendPost([i[1], i[4], i[5], i[0]], call.message.chat.id)
                    time.sleep(random.randint(2, 5))
            bot.send_message(call.message.chat.id, "Вот все вопросы")

    if (values == "chek_new"):
            print(Chek_mas)
            for i in Chek_mas:
                if (i[6] == 0 and i[3] == 0):
                    bot.send_message(call.message.chat.id,f"пост под номером {i[0]}")
                    MediaSendPost([i[1], i[4], i[5], i[0]], call.message.chat.id)
                    time.sleep(random.randint(2, 5))
            bot.send_message(call.message.chat.id, "Вот все вопросы")


def DelName(message):
    #print(message.entities[0].url)-получение url
    if ("/" in message.text):
        bot.send_message(message.chat.id, "Канал не может начинаться с /")
    else:
        if(Chek(message.text)):
            db = sqlite3.connect("Media.db")
            Base = DataBaseChannels(db)
            Base.Delete(message)
            Base.Close()
            st = PrintName()[1]
            bot.send_message(message.chat.id, f"Каналы которые остались:"+st)
        else:
            bot.send_message(message.chat.id, f"Вы пытаетесь удалить канал которого нет")
            #bot.send_message(message.chat.id, "Напишите Название канала для удвления")
            #bot.register_next_step_handler(message, DelName)


def Chek(name):
    f=False
    db = sqlite3.connect("Media.db")
    Base = DataBaseChannels(db)
    mas = Base.Fetch()
    for i in mas:
        if(name == i[1]):
            f=True
    Base.Close()
    return f


def PrintName():
    db = sqlite3.connect("Media.db")
    Base = DataBaseChannels(db)
    mas = Base.Fetch()
    Base.Close()
    mas_p=[]
    for i in mas:
        mas_p.append(i[1])
    st = ""
    for i in mas_p:
        st += "\n" + " " + i
    return mas_p, st


def MediaSendPost(path_quantity, idChat):
    text, path, quantity, id_ = path_quantity[0], path_quantity[1], path_quantity[2], path_quantity[3]
    media=[]
    try:
        if(path==""):
            bot.send_message(idChat, text)
        else:
            for i in range(quantity):
                try:
                    pic = open(path+str(i)+".jpg", "rb")
                    if(i==0):
                        if(len(text)>1000):
                            text = text[:1000]
                            print("big")
                        media.append(InputMediaPhoto(pic,caption=text))
                    else:
                        media.append(InputMediaPhoto(pic))

                except:
                    pic = open(path + str(i) + ".mp4", "rb")
                    if (i == 0):
                        if (len(text) > 1000):
                            text = text[:1000]
                            print("big")
                        media.append(InputMediaVideo(pic, caption=text))
                    else:
                        media.append(InputMediaVideo(pic))

            bot.send_media_group(idChat, media)
    except:
        bot.send_message(idChat, "Возможно проблемы с файлами")


def EditMessage(message):
    global SelectPost
    print(SelectPost)
    db = sqlite3.connect("Media.db")
    Base = DataBaseMedia(db)
    Base.UpdateText(SelectPost[0], message.text)
    mas = Base.Select(SelectPost[0])
    Base.Close()
    mas=mas[0]
    MediaSendPost([mas[1],mas[4],mas[5],mas[0]], message.chat.id)

    bot.send_message(message.chat.id, "Вот так будет выглядеть пост")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("Редактировать текст", callback_data='edit_text')
    btn2 = types.InlineKeyboardButton("Все окей можно добавить в очередь", callback_data='keep')
    markup.row(btn1)
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Выбирите дальнейшее действие',
                     reply_markup=markup)

def cycle():
    global time_posts
    while True:
        if(len(time_posts)>40):
            time_posts = time_posts[2:]

        db = sqlite3.connect("Media.db")
        Base = DataBaseMedia(db)
        mas = Base.Fetch()

        for i in range(len(mas)):
                mas[i] = list(mas[i])
                if(mas[i][3] == 1 and mas[i][6] == 0):
                    print(Base.Select(mas[i][0])[0][6], type(Base.Select(mas[i][0])[0][6]), not (Base.Select(mas[i][0])[0][6]>0))
                    t = random.randint(numtime * 60, numtime * 60 + 120)
                    time.sleep(t)
                    print(Base.Select(mas[i][0])[0][6], type(Base.Select(mas[i][0])[0][6]),
                          not (Base.Select(mas[i][0])[0][6] > 0))
                    if(not (Base.Select(mas[i][0])[0][6]>0)):
                        mas[i][6] = 1
                        print(Base.Select(mas[i][0])[0][6], type(Base.Select(mas[i][0])[0][6]))
                        Base.UpdatePublishedChannel(mas[i][0], 1)
                        time_posts.append(mas[i][2])
                        print("asd",Base.Select(mas[i][0]))
                        print(Base.Select(mas[i][0])[0][6], type(Base.Select(mas[i][0])[0][6]))
                        MediaSendPost([mas[i][1], mas[i][4], mas[i][5], mas[i][0]], id_channel)

        Base.Close()


def numChek(nums):
    try:
        if(int(nums)>=0):
            return True
    except:
        return False


def timeChange(message):
    s = message.text
    global numtime
    if(numChek(s)):
        numtime = int(s)
        bot.send_message(message.chat.id, "Записал время")
    else:
        bot.send_message(message.chat.id, "Проверьте число")

def prefstart(message):
    bot.send_message(message.chat.id, "Напиши время переодичности публикации в канал в минутах")
    bot.register_next_step_handler(message, timeChange)


bot.polling()