import unittest
from ChatBot import Mail

class MainTest(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # Проверим, что s.split не работает, если разделитель - не строка
        with self.assertRaises(TypeError):
            s.split(2)

    def test_mail_cleaner(self):
        q = Mail()
        text = "П#р@@И*ве%т##"
        q.inbox(message=text)
        ans = q.message
        try_ans = "привет"
        self.assertEqual(ans, try_ans)


if __name__ == '__main__':
    unittest.main()