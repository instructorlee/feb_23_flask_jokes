from app.config.mysqlconnection import connectToMySQL
from datetime import date

class Punchline:

    dB = 'z_jokes'

    def __init__(self, joke_data):
        
        self.id = joke_data['id']
        self.text = joke_data['text']
        self.joke_id = joke_data['joke_id']

    # class level method

    @classmethod
    def get_by_id(cls, id):
        
        query = """
            SELECT 
                * 
            FROM 
                punchlines

            WHERE 
                id=%(id)s
                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, { 'id': id })
        return cls(results[0]) if results else None # double check that something was found
    
    @classmethod
    def get_all(cls):

        query = """
            SELECT 
                * 
            FROM 
             punchlines;
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

                punchlines
                
            (text, joke_id)
            
            VALUES
            (%(text)s, %(joke_id)s)
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, data)

    @classmethod
    def update(cls, data):

        query = """
            UPDATE

                punchlines
                
            SET
                text=%(text)s
                
            WHERE
                id=%(id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, data)

    @classmethod
    def delete(cls, id):
        
        query = """
        DELETE FROM 
            punchlines

        WHERE
            id=%(id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, { 'id': id })