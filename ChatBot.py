import time
import random
import requests
from pyaspeller import Word
import re
from copy import copy
import urllib

dictionary = [
    # ['word', 'action', 'side',  mood, polite, cool]
    # dictionary[0] - первое слово с параметрами, dictionary[0][0] - текст первого слова
    # word - word
    # action: 0 - Hi, 1 - Bye, 2 - Yes, 3 - No, 4 - как дела
    # side: 0 - questioner, 1 - respondent, 2 - anyway
    # mood, polite, cool - quality bot/man. type: integer. change range: [-100; 100]

    ["hi",              0, 2, 2, 0, 0],
    ["привет",          0, 2, 2, 0, 0],
    ["дороу",           0, 2, 2, 0, 0],
    ["здрасте",         0, 2, 2, 0, 0],
    ["пока",            1, 2, 2, 0, 0],
    ["увидимся",        1, 2, 2, 0, 0],
    ["да",              2, 2, 2, 0, 0],
    ["дя",              2, 2, 2, 0, 0],
    ["согласен",        2, 2, 2, 0, 0],
    ["ок",              2, 2, 2, 0, 0],
    ["нет",             3, 2, 2, 0, 0],
    ["не согласен",     3, 2, 2, 0, 0],
    ["найн",            3, 2, 2, 0, 0],
    ["как дела",        4, 0, 2, 0, 0],
    ["как ты",          4, 0, 2, 0, 0],
    ["хорошо",          4, 1, 2, 0, 0],
    ["отлично",         4, 1, 2, 0, 0],
    ["плохо",           4, 1, 2, 0, 0],
    ["почему",          5, 0, 2, 0, 0],
    ["из-за чего",      5, 0, 2, 0, 0],
    ["не знаю",         5, 1, 2, 0, 0],
    ["хз",              5, 1, 2, 0, 0],
    ["настроения нет",  5, 1, 2, 0, 0],
    ["как зовут",       6, 0, 2, 0, 0],
    ["как звать",       6, 0, 2, 0, 0],
    ["{name}",            6, 1, 2, 0, 0],
    ["меня зовут {name}", 6, 1, 2, 0, 0],
    ["сколько тебе лет",  7, 0, 2, 0, 0],
    ["мне {age} лет",     7, 1, 2, 0, 0],
    ["сколько времени",   8, 0, 2, 0, 0],
    ["время",             8, 0, 2, 0, 0],
    ["Сейчас {time} по UNIX",   8, 1, 2, 0, 0],


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
        self.language = "ru-Ru"
        self.speaker = "zahar"  # alyss
        self.type_answer = "text"  # text or voice

        self.api_request = "{host}?text={text}&format={format}&lang={lang}&speaker={speaker}&emotion={mood}&key={key}"
        self.api_key = "151d7f5a-da6d-4564-84eb-0a93b300d688"
        self.api_format = "mp3"
        self.api_host = "https://tts.voicetech.yandex.net/generate"

        self.mood = 70
        self.polite = 50
        self.cool = 80

        self.last_message = ""
        self.to_do_actions = []
        self.to_do_sides = []
        self.dry_words = []
        self.words = []
        self.text = ""
        self.sentences = []

        self.static_answer = ""
        self.dynamic_answer = ""

        self.data = {}
        self.upload_data()

    def __str__(self):
        return "I'm bot"

    def get_time(self):
        return int(time.time())

    def upload_data(self):
        self.data = {
            'Name': self.name,
            'Age': self.age,
            "Time": self.get_time(),
        }

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
        self.what_to_do()

    def set_posion_answer(self, start_pos):
        if start_pos == 0:
            return 1
        elif start_pos == 1:
            return 0
        else:
            return 2

    def what_to_do(self):
        for sen in self.sentences:
            for dict_word in dictionary:
                if sen == dict_word[0]:   # если есть в словаре - добавляем в to do лист
                    self.to_do_actions.append(dict_word[1])
                    self.to_do_sides.append(self.set_posion_answer(start_pos=dict_word[2]))
                    # запоминаем, в какой позиции нужно ответить (side)

    def get_param_dictionary_by_word(self, word, pos):
        for i in dictionary:
            if i[0] == word:
                return i[pos]

    def review_response(self):
        answer = ""
        new_answer = ""
        array_my_action = []
        param = []
        kol = 0  # количество прокруток цикла, отсчет с 0
        for action in self.to_do_actions:  # узнаем значение (экшен) ответа
            for word in dictionary:  # достаем все слова с парам. из нашего словаря
                param = copy(word)  # записывем массив параметров этого слова в param
                if param[1] == action and param[2] == self.to_do_sides[kol]:
                    # todo: исправить вылет приложения при отсутствии ответа
                    # если значение слова словаря со значением слова из предожения и служит ответом
                    if param[2] == 0:
                        stroka = param[0] + "?"
                    else:
                        stroka = param[0] + "."
                    array_my_action.append(stroka)  # записываем само слово в массив слов с нужным знач
            new_answer = random.choice(array_my_action)  # выбираем рандомный ответ из словаря с опред. экшеном
            # todo: повышать регистр только первого слова
            answer = answer + " " + new_answer.title()  # записываем ответ на конкретное слово в текст ответа
            array_my_action = []  # чистим временные словари
            param = []
            kol += 1
        new_answer = ""

        answer = answer[1:]
        if answer == "":  # бот не может ответить ни на одну фразу. Отвечаем готовой фразой
            answer = random.choice(no_answer)
        return answer

    def response(self):
        self.static_answer = self.review_response()
        self.after_response()

        self.upload_data()
        self.dynamic_answer = self.static_answer.format(**self.data)

        if self.type_answer == "text":
            return self.text_response()
        elif self.type_answer == "voice":
            return self.voice_response()
        else:
            return "Некорректный тип ответа"

    def text_response(self):
        return self.dynamic_answer

    def voice_response(self):
        text_in_url_format = urllib.parse.quote(self.dynamic_answer)
        api_data = {
            'host': self.api_host,
            'text': text_in_url_format,
            'key': self.api_key,
            'speaker': self.speaker,
            'lang': self.language,
            'mood': "good",
            'format': self.api_format,
        }
        speak_answer = self.api_request.format(**api_data)
        return speak_answer

    def after_response(self):
        self.last_message = ""
        self.to_do_actions = []
        self.to_do_sides = []
        self.dry_words = []
        self.words = []
        self.text = ""
        self.sentences = []
        self.answer = ""


class Mail(object):
    def __init__(self):
        self.bot = Bot()
        self.message = "No message"

    def __str__(self):
        return "I'm mail manager"

    def cleaner_message(self):
        mess = self.message.lower()
        mess = re.sub(r"[#%@*]", "", mess)
        self.message = mess

    def inbox(self, message):
        if message:
            self.message = message
        self.cleaner_message()
        self.bot.listen(message=self.message)

    def outbox(self):
        return self.bot.response()
