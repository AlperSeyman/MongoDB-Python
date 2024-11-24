from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient



load_dotenv(find_dotenv())
printer = pprint.PrettyPrinter()

class FullText():
    def __init__(self, query):
        self.password = os.environ.get("")
        self.client = self.connect_db()
        self.query = query
    
    
    def connect_db(self):
        try:
            connection_string = f""
            client =  MongoClient(connection_string)
            jeoprady_db = client.jeoprady_db # Access the database
            questions = jeoprady_db.questions
            return questions
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise
    
    def fuzzy_matching(self):
        questions = self.connect_db()
        result = questions.aggregate([
            {
                "$search":{
                    "index":"language_search",
                    "text": {                # text-based search
                        "query": self.query, # search for "computer""
                        "path": "category",  # search  for "computer" in the "category" field.
                        "fuzzy":{}
                    }
                }
            }
        ])
        printer.pprint(list(result))




    def autocomplete(self):
        questions = self.connect_db()
        result = questions.aggregate([
            {
                "$search": {
                    "index": "language_search",
                    "autocomplete": {
                        "query": self.query,
                        "path": "question",
                        "tokenOrder": "sequential",
                        "fuzzy": {}
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "question": 1
                }
            }
        ])
        printer.pprint(list(result))


    
print(""" 
        ...... Exit for write 'e' and enter ......
        ...... Select Searching Engine ......
          1-) aotocomplete 
          2-) fuzzy matching
          """)
engine = input("Entet your engine: ")
while True:
    query = input("Enter your sentence: ")
    if query  == "e":
        break
    results = FullText(query=query)
    if engine == "aotocomplete":
            results.autocomplete()
            print("...... Exit for write 'e' and enter ......") 
    if engine == "fuzzy matching":
            results.fuzzy_matching()
            print("...... Exit for write 'e' and enter ......") 
         



