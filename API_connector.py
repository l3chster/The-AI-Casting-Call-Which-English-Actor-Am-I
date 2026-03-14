from dotenv import load_dotenv
import requests
import os
import db_connector
from embeddings import Person
from insightface.app import FaceAnalysis

load_dotenv()

'''
I`m connecting with TMDB API which is website with cinematic info: actors, directors, films, ....
'''

model = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
API_KEY = os.getenv("API_KEY") 
url = "https://api.themoviedb.org/3/person/popular" 

how_many_pages = 300    # I set limit to first 3 pages 

'''
Here we've got about 225 000 pages with 4.5 million actors around the world so I've taken into
consideration first 300 (they are sorted by popularity so famous actors will be added) to fill my database
'''


new_db = db_connector.DB_connection()   # creating new database connection
count = 1


for i in range(1,how_many_pages):
    params = {
    "api_key": API_KEY,     
    'language' : 'en-US',
    'page' : f'{i}',           # i stands for number of page
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:              # if there is an error with API request we`ll get status code different than 200 and we`ll break the loop
        break


    data = response.json()                       # json file                 
    
    for x in range(len(data['results'])):                # len(data['results']) is equal to number of actors on page
        popularity = data['results'][x]['popularity']
        if popularity > 3.4:           
            
            actor_language = data['results'][x]['known_for'][0]['original_language'] 

            if actor_language == 'en' and data['results'][x]['profile_path']:    #we`re taking only actors who speak english and with photo link             
                    link = "https://image.tmdb.org/t/p/w500" + data['results'][x]['profile_path']  

                    person = Person(data['results'][x]['name'])                   
                   
                    print(count, link, person.name, person.last_name, popularity)                 

                    img_embedding = person.get_embedding(model, whole_link=link) 

                    if img_embedding:    
                        new_db.add_person_to_db(person.name, person.last_name, img_embedding, popularity)                    
                        count+=1

                
                

            
