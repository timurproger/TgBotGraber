from program.tokens import mas_tokens
import time
from datetime import datetime
from datetime import date
from pyrogram import Client
from program.DataBase import DataBaseMedia, DataBaseChannels
import sqlite3

api_hash = mas_tokens[0]
api_id = mas_tokens[1]

client = Client(name="my_client", api_id=api_id, api_hash=api_hash)


def ParsingMessage(name_channel):
    db = sqlite3.connect("Media.db")
    Base = DataBaseMedia(db)
    mas = Base.Fetch()
    client.start()
    Base.Close()
    mas_mes=[]
    for message in client.get_chat_history(chat_id=name_channel, limit=50):
        time_p = message.date

        if(ChekOnTime(mas, time_p)):
            p = saveMessage(message)
            if(p!=None):
                mas_mes.append(p)

    print(mas_mes)
    if(len(mas_mes)>0):
        saveInBase(mas_mes)

    client.stop()


def saveMessage(message):
    mas = None
    try:

        if (message.photo != None):
            print(message.photo.file_id)
            if (message.caption != None):
                txt = message.caption
            else:
                txt = message.text
            #print(message.entities[0].url, "фото")
            #print(message.caption, message.date.time())
            time_p = message.date

            mas = [time_p, message.photo.file_id, txt, 'chosen_order' in str(message.reactions), "photo"]

        elif (message.video != None):
            if (message.caption != None):
                txt = message.caption
            else:
                txt = message.text
            #print(message.video, "фото")
            #print(message.caption, message.date.time())
            time_p = message.date

            mas = [time_p, message.video.file_id, txt, 'chosen_order' in str(message.reactions), "video"]
        elif(message.text != None):
            time_p = message.date
            txt = message.text
            mas = [time_p, "", txt, 'chosen_order' in str(message.reactions), "text"]

    except:
        pass
    return mas


def saveInBase(mas):
    db = sqlite3.connect("Media.db")
    Base = DataBaseMedia(db)

    fil_photos = []

    for i in mas:
        print(i,"dkfs")
        if (i[2] == None):
            fil_photos.append(i)
        elif (i[3] == True):
            k = 0
            fil_photos.append(i)
            date_posts = date.today()
            time_posts = datetime.now().strftime('%H-%M-%S')

            text_posts = ""
            time_post = None
            t = f"downloads\\{date_posts}\\{time_posts}\\"

            for j in fil_photos:
                if (j[4] == "photo"):
                    client.download_media(j[1],
                                              file_name=f"{t}{k}.jpg")
                elif (j[4] == "video"):
                    client.download_media(j[1],
                                              file_name=f"{t}{k}.mp4")
                elif (j[4] == "text"):
                    t = ""

                k += 1

                if (j[2] != None):
                        time_post = j[0]
                        text_posts = j[2]
            Base.AddIntoDB(text_posts, time_post, False, f"{t}", k, False)
                # print(Base.Fetch())
            fil_photos.clear()

        elif (i[3] == False):
            fil_photos.clear()

    Base.Close()


def ChekOnTime(mas, time_p):
    # print(mas)
    f = True
    for i in mas:
        #print(i[2],time_p, type(i[2]), type(time_p))
        if (i[2] == str(time_p)):
            f = False

    return f


def mainNames():
    while True:
        mas = PrintName()
        for i in mas:
            print(i)
            ParsingMessage(i)
        time.sleep(60)


def PrintName():
    db = sqlite3.connect("Media.db")
    Base = DataBaseChannels(db)
    mas = Base.Fetch()
    Base.Close()
    mas_p = []
    for i in mas:
        mas_p.append(i[1])
    return mas_p


mainNames()