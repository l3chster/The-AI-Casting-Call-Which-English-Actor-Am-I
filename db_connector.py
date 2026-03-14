import psycopg2
import os
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()  # we`re loading variables from .env file

'''
we use DB_connection to connect to database and gain embedding which is the vector of float values. These float values are 
coords (specific for each person). To avoid taking ID card data from people, I simplified the situation (there can not be 
2 people with the same name and surname in database)


I created hnsw indexes so that comparing embeddings is faster and more efficient
(create index on actors using hnsw (embedding vector_cosine_ops));
'''


class DB_connection: 

    def __init__(self):
        '''
        connecting with local database
        '''        
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")


        self.mydb = psycopg2.connect(host=self.DB_HOST,port=self.DB_PORT, user=self.DB_USER, password=self.DB_PASSWORD, database=self.DB_NAME)   
        self.my_cursor = self.mydb.cursor()  # cursor is a tool to send commands over to the database

    def get_embedding(self, name, last_name):        
          
        '''
        table actors has columns: name, last_name, popularity, embedding              
        '''                  
        
        self.my_cursor.execute(f"SELECT embedding FROM actors WHERE name = '{name}' AND last_name = '{last_name}' ")           
        my_result = self.my_cursor.fetchall() # fetches all (or all remaining) rows of a query result set and returns a list of tuples (1 row = 1 tuple)
        return my_result[0][0]
    
    
    def add_person_to_db(self, name, last_name, embeding, popularity):

        '''
        This method is for adding new person to database
        '''          

        self.my_cursor.execute(f"""INSERT INTO actors (name, last_name, embedding, popularity)
        VALUES ('{name}', '{last_name}', '{embeding}', {popularity})
        """)       
        
        self.mydb.commit()
        print(self.my_cursor.rowcount, "record inserted.")      

        
    
    def find_closest_embedding(self, embedding, threshold=0):       
        '''
        This method is for finding the closest embedding (cosine similarity) 
        in database to the given embedding (the one we want to compare with)

        threshold range (3.4 - 50.42)  However 5 highest scores: 50.42, 35.21, 24.82, 23.56, 21.67
        '''           
        
        self.my_cursor.execute(f"""SELECT name, last_name, (embedding <=> '{embedding}') AS similarity
        FROM actors
        WHERE popularity > {threshold}                       
        ORDER BY embedding <=> '{embedding}' ASC        
        LIMIT 1;                         
        """)           
        my_result = self.my_cursor.fetchall() 
        return my_result[0][0], my_result[0][1], round((1 - my_result[0][2]) * 100, 2)    

        





 

