import time
import random
import requests
from pyaspeller import Word
import re
from copy import copy

dictionary = [
    # ['word', 'action', 'side',  mood, polite, cool]
    # dictionary[0] - первое слово с параметрами, dictionary[0][0] - текст первого слова
    # word - word
    # action: 0 - Hi, 1 - Bye, 2 - Yes, 3 - No, 4 - как дела
    # side: 0 - questioner, 1 - respondent, 2 - anyway
    # mood, polite, cool - quality bot. type: integer. change range: [-100; 100]

    ["hi",          0, 2, 2, 5, 2, 0],
    ["привет",      0, 2, 2, 5, 2, 0],
    ["дороу",       0, 2, 2, 5, 2, 2],
    ["здрасте",     0, 2, 2, 5, 2, 2],
    ["пока",        1, 2, 2, 5, 2, 0],
    ["увидимся",    1, 2, 2, 5, 2, 0],
    ["да",          2, 2, 2, 1, 0, 0],
    ["согласен",    2, 2, 2, 1, 0, 0],
    ["ок",          2, 2, 2, 1, 0, 0],
    ["нет",         3, 2, 2, -1, 0, 0],
    ["не согласен", 3, 2, 2, -1, 0, 0],
    ["найн",        3, 2, 2, -1, 0, 1],
    ["как дела",    4, 0, 2, -1, 0, 1],
    ["как ты",      4, 0, 2, -1, 0, 1],
    ["хорошо",      4, 1, 2, -1, 0, 1],
    ["отлично",     4, 1, 2, -1, 0, 1],
    ["плохо",       4, 1, 2, -1, 0, 1],

]


no_answer = [
    "прости, я не понял тебя :(",
    "я тебя не понимаю",
    "мне нечего ответить..."
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
        self.cool = 80

        self.last_message = ""
        self.to_do_actions = []
        self.dry_words = []
        self.words = []
        self.text = ""
        self.sentences = []

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

    def sentence_breaking(self):
        split_regex = re.compile(r'[.,|!|?|…]')
        self.sentences = filter(lambda t: t, [t.strip() for t in split_regex.split(self.text)])
        # self.print_sentences()

    def print_sentences(self):
        for s in self.sentences:
            print(s)

    def get_clean_text(self):
        s = ""
        for i in self.words:
            s = s + " " + i
        self.text = s[1:]

    def search_word_in_dictionary(self, word):
        for q in dictionary:
            if q[0] == word:
                return True  # найдено
        return False  # не найдено

    def auto_corrector(self):
        for dry_word in self.dry_words:
            if self.search_word_in_dictionary(word=dry_word):
                self.words.append(dry_word)
                break  # если нашли это слово в нашем словаре - не чекаем и не исправляем его (обычно - это сленг)

            check = Word(dry_word)
            if not check.correct:
                if not check.variants == []:
                    self.words.append(check.variants[0])
            else:
                self.words.append(dry_word)

    def review_listen(self):
        self.dry_word_breaking()
        self.auto_corrector()
        self.word_breaking()
        self.get_clean_text()
        self.sentence_breaking()
        # todo: научиться понимать несколько фразы, а не только слова. Пример: Как дела?
        self.what_to_do()

    def what_to_do(self):
        for sen in self.sentences:
            for dict_word in dictionary:
                if sen == dict_word[0]:   # если есть в словаре - добавляем в to do лист
                    self.to_do_actions.append(dict_word[1])

    def what_to_do_old(self):
        for mess_word in self.words:            # берем слово из сообщения
            for dict_word in dictionary:        # берем слово из словаря
                if mess_word == dict_word[0]:   # если есть в словаре - добавляем в to do лист
                    self.to_do_actions.append(dict_word[1])
                else:
                    pass                        # этого слова пока нет в нашем словаре. (для дальнейшей разработки)

    def response(self):
        answer = ""
        new_answer = ""
        array_my_action = []
        param = []

        for action in self.to_do_actions:   # узнаем значение (экшен) ответа
            for word in dictionary:         # достаем все слова с парам. из нашего словаря
                param = copy(word)          # записывем массив параметров этого слова в param
                if param[1] == action:      # если значение слова словаря со значением слова из предожения
                    array_my_action.append(param[0])     # записываем само слово в массив слов с нужным знач
            new_answer = random.choice(array_my_action)  # выбираем рандомный ответ из словаря с опред. экшеном
            answer = answer + " " + new_answer + "."     # записываем ответ на конкретное слово в текст ответа
            array_my_action = []                         # чистим временные словаря
            param = []
        new_answer = ""

        answer = answer[1:]
        if answer == "":                    # бот не может ответить ни на одну фразу. Отвечаем готовой фразой
            answer = random.choice(no_answer)

        full_answer = "Твое сообщение: " + self.last_message + "\n" + "Мой ответ: " + answer
        self.clean_after_answer()
        return answer  # full_answer - debug, answer - release

    def clean_after_answer(self):
        self.last_message = ""
        self.to_do_actions = []
        self.dry_words = []
        self.words = []
        self.text = ""
        self.sentences = []


class Mail(object):
    def __init__(self):
        self.bot = Bot()
        self.message = "No message"

    def __str__(self):
        return "I'm mail manager"

    def cleaner_message(self):
        mess = self.message.lower()
        # mess = re.sub(r"[#%!@*.,?]", "", mess)
        self.message = mess

    def inbox(self, message):
        if message:
            self.message = message
        self.cleaner_message()
        self.bot.listen(message=self.message)

    def outbox(self):
        return self.bot.response()
