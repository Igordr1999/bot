import time
import random
import requests
from pyaspeller import Word

man_hi_words = [
    "дороу",
    "привет",
    "hi",
    "здарова",
]

man_bye_words = [
    "пока",
    "покеда",
]

actions = [
    "hi",
    "bye"
]

robot_hi = [
    "Добрый вечер, я робот ^_^",
    "Дороу",
    "Дратути",
    "Здрасте",
]

robot_bye = [
    "Пока :(",
    "Ну ладно. Увидимся)",
    "Покеда",
]
robot_dont_answer = [
    "Прости, я не понял тебя :(",
    "Я тебя не понимаю",
    "Не понял, напиши еще раз",
]


class Bot(object):
    def __init__(self):
        self.name = "Вася"
        self.last_name = "Петров"
        self.age = 18
        self.sex = "Man"
        self.language = "RU"

        self.mood = 70
        self.polite = 50

        self.last_message = ""
        self.to_do_actions = ""
        self.dry_words = []
        self.words = []

    def __str__(self):
        return "I'm bot"

    def listen(self, message):
        self.last_message = message
        self.review_listen()

    def dry_word_breaking(self):
        self.dry_words = self.last_message.split(' ')

    def word_breaking(self):
        my_str = ""
        for i in self.words:
            my_str = my_str + " " + i
        my_str = my_str[1:]
        self.words = my_str.split(' ')

    def auto_corrector(self):
        for i in self.dry_words:
            check = Word(i)
            if not check.correct:
                if not check.variants == []:
                    self.words.append(check.variants[0])
            else:
                self.words.append(i)

    def review_listen(self):
        self.dry_word_breaking()
        self.auto_corrector()
        self.word_breaking()
        print(self.words)
        for i in self.words:
            if man_hi_words.count(i):
                self.to_do_actions = "hi"
            if man_bye_words.count(i):
                self.to_do_actions = "bye"

    def response(self):
        answer = ""
        if self.to_do_actions == "hi":
            answer = random.choice(robot_hi)
        if self.to_do_actions == "bye":
            answer = random.choice(robot_bye)
        if self.to_do_actions == "":
            answer = random.choice(robot_dont_answer)
        full_answer = "Твое сообщение: " + self.last_message + "\n" + "Мой ответ: " + answer
        self.clean_after_answer()
        return answer  # full_answer - debug, answer - release

    def clean_after_answer(self):
        self.last_message = ""
        self.to_do_actions = ""
        self.dry_words = []
        self.words = []


class Mail(object):
    def __init__(self):
        self.bot = Bot()
        self.message = "No message"
        self.cleaner_message()

    def __str__(self):
        return "I'm mail manager"

    def cleaner_message(self):
        return self.message.lower()

    def inbox(self, message):
        if message:
            self.message = message
        self.bot.listen(message=self.message)

    def outbox(self):
        return self.bot.response()
