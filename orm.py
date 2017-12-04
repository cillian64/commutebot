import peewee


db = peewee.SqliteDatabase('commutebot.sqlite3')


class Trial(peewee.Model):
    timestamp = peewee.DateTimeField()
    duration = peewee.IntegerField()
    scheduledtime = peewee.FixedCharField(4)
    start = peewee.CharField()
    end = peewee.CharField()

    class Meta:
        database = db


# This does nothing if the table already exists
db.create_tables([Trial], safe=True)
