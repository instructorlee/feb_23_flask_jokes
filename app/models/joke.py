from app.config.mysqlconnection import connectToMySQL
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
    def create(cls, data):

        query = """
            INSERT INTO

                jokes
                
            (text, punchline)
            
            VALUES
            (%(text)s, %(punchline)s)
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