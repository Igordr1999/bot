import time


class Bot(object):
    def __init__(self):
        self.name = "Vasya"
        self.last_name = "Petrov"
        self.age = 18
        self.sex = "Man"
        self.language = "RU"

        self.mood = 70
        self.polite = 50

        self.last_message = ""

    def __str__(self):
        return "I'm bot"

    def listen(self, message):
        self.last_message = message

    def response(self):
        return "My response: " + self.last_message + " too ^_^"


class Mail(object):
    def __init__(self):
        self.bot = Bot()
        self.message = "qq"
        self.cleaner_message()
        # self.inbox()
        # self.outbox()

    def __str__(self):
        return "I'm mail manager"

    def cleaner_message(self):
        return self.message

    def inbox(self, message):
        if message:
            self.message = message
        self.bot.listen(message=self.message)

    def outbox(self):
        return self.bot.response()
