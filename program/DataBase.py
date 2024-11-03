import sqlite3


class DataBaseMedia():

    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS media (
                    text_post text,
                    time timestamp,
                    published boolean,
                    image_path text,
                    count_image integer,
                    published_channel boolean
                )""")

    def AddIntoDB(self,text, time, published, image_path, count, published_channel):
        sqlite_insert_with_param = "INSERT INTO media VALUES(?, ?, ?, ?, ?, ?)"
        data_tuple = (text, time, published, image_path, count, published_channel)
        self.cursor.execute(sqlite_insert_with_param, data_tuple)
        self.db.commit()

    def Fetch(self):
        self.cursor.execute("SELECT rowid,* FROM media")
        ins = self.cursor.fetchall()
        mas=[]
        for i in ins:
            mas.append(i)
        return mas

    def Delete(self,delete_id):
        self.cursor.execute(f"DELETE FROM media WHERE rowid > {delete_id}")
        self.db.commit()

    def UpdateText(self, up_id, new_text):
        self.cursor.execute(f'UPDATE media SET text_post = "{new_text}" WHERE rowid = {up_id}')
        self.db.commit()

    def UpdatePublished(self, up_id, published):
        self.cursor.execute(f"UPDATE media SET published = '{published}' WHERE rowid = {up_id}")
        self.db.commit()

    def UpdatePublishedChannel(self, up_id, published):
        self.cursor.execute(f"UPDATE media SET published_channel = '{published}' WHERE rowid = {up_id}")
        self.db.commit()

    def Select(self, ID):
        self.cursor.execute(f"SELECT rowid,* FROM media WHERE rowid = {ID}")
        ins = self.cursor.fetchall()
        return ins

    def Close(self):
        self.cursor.close()
        self.db.close()


class DataBaseChannels():

    def __init__(self, db):
        self.db = db
        self.cursor = self.db.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS channels (
                            channel_names text
                        )""")

    def AddIntoDB(self,name):
        sqlite_insert_with_param = f"INSERT INTO channels VALUES(?)"
        data_tuple = (name,)
        self.cursor.execute(sqlite_insert_with_param, data_tuple)
        self.db.commit()

    def Fetch(self):
        self.cursor.execute("SELECT rowid,* FROM channels")
        ins = self.cursor.fetchall()
        mas=[]
        for i in ins:
            mas.append(i)
        return mas

    def Delete(self, delete_name):
        self.cursor.execute(f"DELETE FROM channels WHERE channel_names = '{delete_name}'")
        self.db.commit()

    def Close(self):
        self.cursor.close()
        self.db.close()


'''db = sqlite3.connect("Media.db")
Base = DataBaseChannels(db)
#Base.Delete(2)
Base.AddIntoDB("INSTARDING")
print(Base.Fetch())
Base.Close()
published_channel boolean,'''

'''db = sqlite3.connect("Media.db")
Base = DataBaseMedia(db)
Base.Delete(0)
print(Base.Fetch())
Base.Close()
'''
'''db = sqlite3.connect("Media.db")
Base = DataBaseMedia(db)

print(Base.Select(1))
Base.Close()'''

db = sqlite3.connect("../Media.db")
Base = DataBaseMedia(db)
for i in Base.Fetch():
    print(i)
Base.Close()