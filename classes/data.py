import json
import os

class Data:

    def __init__(self, data_file_name):
        self.data_file_name = data_file_name

    def get(self):

        # try statements allow us to execute code that we know could result in an error.
        try: 
            with open(f'{self.data_file_name}.json', 'r') as openfile:
                return json.load(openfile) #Loads JSON and converts it to an object

        except Exception as e: # If there is an error, alternate code is executed
            data = []

        return data
        

    def save(self, data):

        try:
            os.remove(f'{self.data_file_name}.json')
        except:
            pass # Python requires code after a line that ends in ':'. PASS is a Python placeholder

        try: 
            with open(f'{self.data_file_name}.json', 'w') as outfile:
                outfile.write(json.dumps(data)) # converts object to JSON and saves it

            return True

        except Exception as e: # can save error a message that can be displayed
            print(f'save error: {e}')
            return False