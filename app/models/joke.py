from app.config.mysqlconnection import connectToMySQL
from app.models.punchline import Punchline

class Joke:

    dB = 'z_jokes'

    def __init__(self, joke_data):
        
        self.id = joke_data['id']
        self.user_id = joke_data['user_id']
        self.date_added = joke_data['date_added']
        self.text = joke_data['text']

        #self.punchline = joke_data['punchline']

        self.punchlines = []

    # class level method

    @classmethod
    def get_by_id(cls, id):
        
        query = """
            SELECT 
                * 
            FROM 
                jokes

            LEFT JOIN punchlines ON punchlines.joke_id = jokes.id

            WHERE 
                jokes.id=%(id)s
                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, { 'id': id })

        if results:
            joke = cls(results[0])
            
            for result in results:
                joke.punchlines.append(Punchline({
                    'id': result['punchlines.id'],
                    'text': result['punchlines.text'],
                    'joke_id': joke.id
                }))

            return joke

        return None

        

        # return cls(results[0]) if results else None # double check that something was found
    
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
    def create(cls, data):

        query = """
            INSERT INTO

                jokes
                
            (text, punchline, user_id)
            
            VALUES
            (%(text)s, %(punchline)s, %(user_id)s)
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, data)

    @classmethod
    def update(cls, data):

        query = """
            UPDATE

                jokes
                
            SET
                text=%(text)s,
                punchline=%(punchline)s
                
            WHERE
                id=%(id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, data)

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