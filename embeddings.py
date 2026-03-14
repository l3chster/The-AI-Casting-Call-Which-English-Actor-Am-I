from PIL import Image
import re
from io import BytesIO
import requests
from insightface.app import FaceAnalysis
import cv2
import torch
import numpy as np


class Person:    
    
    def __init__(self, whole_name):
        self.divide_into_parts(whole_name)


    def divide_into_parts(self, whole_name):
        parts_of_name = re.split(' |\'', whole_name)
        self.name = parts_of_name[0]
        self.last_name = ' '.join(parts_of_name[1:])


    def get_photo(self, whole_link):

        '''
        It's important to convert image from RGB to BGR because open cv works with BGR and if 
        we don`t do that we will get wrong results when we`re trying to get embedding for photo
        '''        

        photo = requests.get(whole_link)
        img = Image.open(BytesIO(photo.content))
        img_np = np.array(img)
        
        open_cv_image = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)      # convertion
        return open_cv_image


    def get_embedding(self, app, photo = None, whole_link=None):  

        '''
        buffalo_l is the name of the model I`m using to get embedding for photo, it`s from insightface library and it`s one
        of the best models for face recognition, it`s also very fast and efficient

        CUDAExecutionProvider is a provider for running models on GPU, it`s very fast and efficient, I`m using it to get 
        embedding for photo because it`s much faster than running on CPU
        '''
        
        app.prepare(ctx_id=0, det_size=(640, 640))    # operations on GPU are faster than on CPU 

        if whole_link:
            faces = app.get(self.get_photo(whole_link))   # detects faces in the photo
        else:
            faces = app.get(photo)   # detects faces in the photo
        
 
        if faces:                                     # checks if there is at least one face in the photo
            faceid_embeds = torch.from_numpy(faces[0].normed_embedding).unsqueeze(0)           
            return faceid_embeds.flatten().tolist()  
        return None




