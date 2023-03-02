from config.mysqlconnection import connectToMySQL
from datetime import date

class Joke:

    dB = 'z_jokes'

    def __init__(self, joke_data):
        
        self.id = joke_data['id']
        self.date_added = joke_data['date_added']
        self.text = joke_data['text']
        self.punchline = joke_data['punchline']

    # class level method

    @classmethod
    def get_by_id(cls, id):
        
        query = """
            SELECT 
                * 
            FROM 

                z_jokes.jokes

            WHERE
                id=%(id)s
                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, { 'id': id })

        """
        if results:
            return cls(results[0])

        return None

        """

        return cls(results[0]) if results else None # double check that something was found
    
    @classmethod
    def get_all(cls):

        query = """
            SELECT 
                * 
            FROM 
            z_jokes.jokes;
        """

        results = connectToMySQL(cls.dB).query_db(query)

        """
        rows = []

        for result in results:
            rows.append(cls(result))

        return rows
        """

        return [cls(result) for result in results] # List Comprehension
        
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
        
        query = """
        DELETE FROM 
            z_jokes.jokes

        WHERE
            id=%(id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, { 'id': id })