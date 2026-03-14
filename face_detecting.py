import sys
from embeddings import Person
from db_connector import DB_connection
from insightface.app import FaceAnalysis
import cv2

'''
Here we can find main part of the project, where you need to put your data 
and test the program.
'''

if __name__ == "__main__":

    model = FaceAnalysis(name="buffalo_l", providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])

    name_surname = sys.argv[1]   

    person = Person(name_surname)
    image = cv2.imread(sys.argv[2]) 
    embedding = person.get_embedding(model, photo=image)

    n_db = DB_connection()    
        

    n,s, similarity = n_db.find_closest_embedding(embedding,sys.argv[3] if len(sys.argv) == 4 else 0)
    print(f"Found closest match: {n} {s} with similarity {similarity}%")
