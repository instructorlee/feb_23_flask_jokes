from classes.data import Data
from datetime import date

class Joke:

    jokes = [] # class level attribute

    data_source = Data('jokes_data')

    def __init__(self, joke_data):
        
        self.date_added = joke_data['date_added']
        self.text = joke_data['text']
        self.punchline = joke_data['punchline']

        Joke.jokes.append(self)

    # instance level methods
    def say(self):
        print(f"{self.text} : {self.punchline}")

    def serialize(self):
        return({
            'date_added': str(self.date_added),
            'text': self.text,
            'punchline': self.punchline
        })

    def my_method(self):
        return 'hello world!'

    # class level method

    @classmethod
    def get_by_id(cls, id):
        joke = Joke.jokes[id - 1]
        joke.id = id
        return joke
    
    @classmethod
    def get_all(cls):
        return [{
            'id': index + 1,
            'text': joke.text,
            'punchline': joke.punchline
        } for index, joke in enumerate(cls.jokes)]
        
    @classmethod
    def load(cls):
        data = Joke.data_source.get()
        [cls(row) for row in data]

    @classmethod
    def save(cls):
        cls.data_source.save([joke.serialize() for joke in cls.jokes])

    @classmethod
    def create(cls, text, punchline):

        new_joke = cls({
            'date_added': date.today(),
            'text': text,
            'punchline': punchline
        })

        cls.save()

        return new_joke

    @classmethod
    def update(cls, id, text, punchline):
         Joke.jokes[id - 1].text = text
         Joke.jokes[id - 1].punchline = punchline
         cls.save()

    @classmethod
    def delete(cls, id):
        del(Joke.jokes[id - 1])
        cls.save()