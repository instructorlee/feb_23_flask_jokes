from app.config.mysqlconnection import connectToMySQL
from app.models.punchline import Punchline

class Joke:

    dB = 'z_jokes'

    def __init__(self, joke_data):
        
        self.id = joke_data['id']
        self.user_id = joke_data['user_id']
        self.date_added = joke_data['date_added']
        self.text = joke_data['text']
        self.likes_count = joke_data['likes_count'] if 'likes_count' in joke_data else 0
        self.is_liked_by_current_user = 'joke_id' in joke_data and joke_data['joke_id'] is not None 

        self.punchlines = []
        self.liked_by = []

    def is_liked_by(self, id):
        found_users = list(filter(lambda user: user.id == id, self.liked_by))
        return len(found_users) > 0

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

    @classmethod
    def get_with_likes(cls, id):
        from app.models.user import User
        
        query = """
            SELECT 
                * 
            FROM 
                jokes

            LEFT JOIN user_like_joke ON user_like_joke.joke_id = jokes.id
            LEFT JOIN users ON users.id = user_like_joke.user_id

            WHERE 
                jokes.id=%(id)s
                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, { 'id': id })

        if results:
            joke = cls(results[0])
            
            for result in results:
                if result['users.id']: # in case no likes
                    joke.liked_by.append(User({
                        'id': result['users.id'],
                        'first_name': result['first_name'],
                        'last_name': result['last_name'],
                        'email_address': result['email_address'],
                        'password': result['password']
                    }))

            return joke

        return None

        # return cls(results[0]) if results else None # double check that something was found
    
    @classmethod
    def get_all(cls, user_id):

        query = """
            SELECT 
                *  ,
                (SELECT COUNT(*) FROM user_like_joke WHERE user_like_joke.joke_id = jokes.id) AS likes_count
            FROM 
                z_jokes.jokes

                LEFT JOIN user_like_joke ON user_like_joke.joke_id = jokes.id AND user_like_joke.user_id=%(user_id)s
                LEFT JOIN users ON users.id = user_like_joke.user_id

                ;
        """

        results = connectToMySQL(cls.dB).query_db(query, {'user_id': user_id})

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
    
    @classmethod
    def like(cls, joke_id, user_id):

        query = """
            INSERT INTO

                user_like_joke
                
            (joke_id, user_id)
            
            VALUES
            (%(joke_id)s, %(user_id)s)
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, { 
            'joke_id': joke_id,
            'user_id': user_id
            })

    @classmethod
    def unlike(cls, joke_id, user_id):
        
        query = """
        DELETE FROM 
            user_like_joke

        WHERE
            joke_id=%(joke_id)s AND user_id=%(user_id)s
            ;
        """

        return connectToMySQL(cls.dB).query_db(query, { 
            'joke_id': joke_id,
            'user_id': user_id
            })