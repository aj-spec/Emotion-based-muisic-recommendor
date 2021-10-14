'''
PyPower Projects
Emotion Detection Using AI
'''

#USAGE : python test.py

from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
from cv2 import cv2
import numpy as np

face_classifier = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
classifier =load_model('./Emotion_Detection.h5')

class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

cap = cv2.VideoCapture(0)



while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)


        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

        # make a prediction on the ROI, then lookup the class

            preds = classifier.predict(roi)[0]
            print("\nprediction = ",preds)
            label=class_labels[preds.argmax()]
            print("\nprediction max = ",preds.argmax())
            print("\nlabel = ",label)
            label_position = (x,y)
            arr=[cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)]
        else:
            arr=[cv2.putText(frame,'No Face Found',(20,60),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)]
        print("\n\n")
    cv2.imshow('Emotion Detector',frame)
    print(arr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            from dotenv import load_dotenv
            load_dotenv()
            import spotipy
            from spotipy.oauth2 import SpotifyClientCredentials
            from tkinter import *
            import tkinter as tk
            import webbrowser
            from _ast import Lambda

            def open_spotify(url):
                webbrowser.open(url, new = 2)
            def create_label(text):
                return tk.Label(master = frm_recommendations, text = text)
            def create_button(text, url):
                return tk.Button(master = frm_recommendations, text = text, command = lambda : open_spotify(url))
            def clear(*args):
               args.destroy()
            def display_recommendations(response):
                lbl_track_name = tk.Label(master = frm_recommendations, text = 'Track Name')
                lbl_artist_name = tk.Label(master = frm_recommendations, text = 'Artist Name')
                lbl_play_it = tk.Label(master = frm_recommendations, text = 'Play It')
                lbl_track_name.grid(row = 0, column = 0)
                lbl_artist_name.grid(row = 0, column = 1)
                lbl_play_it.grid(row = 0, column = 2)
            for idx, track in enumerate(response['tracks']):
                lbl_track_name_recommended = create_label(track['name'])
                lbl_track_name_recommended.grid(row = idx +1, column = 0)
                lbl_artist_name_recommended = create_label(track['artists'][0]['name'])
                lbl_artist_name_recommended.grid(row = idx + 1, column = 1)
                btn_play_it_recommended = create_button('Play It', track['external_urls']['spotify'])
                btn_play_it_recommended.grid(row = idx +1, column = 2, padx = 30)

            def get_recommendation():
                search = ent_search.get()
                sp = spotipy.Spotify(client_credentials_manager= SpotifyClientCredentials("4d4a5193b9fd430c94bc51d415e7d785", "5c561eb16dee40a991241a40f3122242"))
                result = sp.search(q = search, limit = 1)
                id_list = [result['tracks']['items'][0]['id']]
                recommendations  =sp.recommendations(seed_tracks = id_list, limit = 20 )
                display_recommendations(recommendations)

            window = tk.Tk()
            frm_search_field  = tk.Frame(master = window, width = 100)
            frm_recommendations = tk.Frame(master = window)
            frm_search_field.pack()
            frm_recommendations.pack()
            ent_search = tk.Entry(master = frm_search_field, width = 25)
            btn_get_recommendations = tk.Button(master = frm_search_field, text = 'Get recommendations', command = get_recommendation ) 	
            ent_search.grid(row = 0,column = 0,pady =  30,padx = 30)
            btn_get_recommendations.grid(row = 0 , column =1, pady = 30, padx = 30)
            window.mainloop()
       

cap.release()
cv2.destroyAllWindows()


























