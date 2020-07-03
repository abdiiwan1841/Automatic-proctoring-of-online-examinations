import pickle
import numpy as np
from PIL import Image
import dlib
from math import sqrt
import cv2
from matplotlib import pyplot as plt 
import subprocess
import timeit

from subprocess import Popen, PIPE
import sys

#Load face encodings
save = open('database/examinee_face_encodings.dat', 'rb')
face_dic = pickle.load(save)
examinee_name = face_dic.keys()[0]
#print examinee_name
pre_encoding = face_dic.values()[0] #there is one encoding only
#print pre_encoding

#ffmpeg stuff
command = "ffmpeg -y -i media/exam/video1.avi -vcodec libx264 -acodec pcm_s16le -ab 160k -ac 1 -ar 48000 -vn audio.wav output.mp4"
subprocess.call(command, shell=True)

""" cmd_list1 = ['python','./audio.py','audio.wav']
p1 = Popen(cmd_list1, stdout=PIPE, stderr=PIPE) """

#Load the video from the disk
input_movie = cv2.VideoCapture('output.mp4')
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(input_movie.get(cv2.CAP_PROP_FPS))
print fps,length

#Create the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_movie = cv2.VideoWriter('media/exam/result/result'+'1'+'.avi', fourcc, fps/16, (640, 480))

#Load the pose predictor model
predictor_model = "models/shape_predictor_68_face_landmarks.dat"
pose_predictor = dlib.shape_predictor(predictor_model)

#Load the face detector model
face_detector = dlib.get_frontal_face_detector()

#Load the face recognition trained model
rec_model = "models/dlib_face_recognition_resnet_model_v1.dat"
facerec = dlib.face_recognition_model_v1(rec_model)

##########
frame_number = 1.0
counter = 0
flag = False
duration = []
face_detection_list = []
frames_list = []

while True:
    print "________________"
    #print len(face_detection_list) , len(frames_list)
    #Set the next frame to read
    input_movie.set(1,frame_number)

    #0-based index of the frame to be decoded/captured next
    current_frame = int(input_movie.get(cv2.CAP_PROP_POS_FRAMES))
    print current_frame
    
    #Read the next frame of video
    ret, frame = input_movie.read()
    start_time = timeit.default_timer()

    #ret=false when there is no frame left
    if not ret:
        print "Video Completed"
        print face_detection_list
        if flag == True:
            duration.append(counter)
            flag = False
            counter = 0
        break

    #Find faces in the frame
    detected_faces = face_detector(frame, 1) #Rectangle object with top(), bottom, left,right
    #print len(detected_faces)

    #Draw a rectangle
    cv2.rectangle(frame, (15,15), (300, 50), (0, 0, 0), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX

    if len(detected_faces) == 0:
        print "No FACE"
        face_detection_list.append(0)
        frames_list.append(current_frame)
        flag = True
        counter = counter + 1
        cv2.putText(frame, "No Face Detected", (15 +20, 15 + 20), font, 0.5, (255, 255, 255), 1)
        # Write the resulting image to the output video file
        output_movie.write(frame)
    
    if len(detected_faces) != 0:
        face_detection_list.append(1)
        if flag == True:
            if counter > 2:
                duration.append(counter)
            print counter
            flag = False
            counter = 0

    if len(detected_faces) > 1:
        print "More Than ONE"
        #face_detection_list.append(2)
        cv2.rectangle(frame, (detected_faces[0].left(), detected_faces[0].top()), (detected_faces[0].right(), detected_faces[0].bottom()), (255, 255, 255), 2)
        cv2.rectangle(frame, (detected_faces[1].left(), detected_faces[1].top()), (detected_faces[1].right(), detected_faces[1].bottom()), (255, 255, 255), 2)
        frames_list.append(current_frame)
        cv2.putText(frame, "More than One Face Detected", (15 +20, 15 + 20), font, 0.5, (255, 255, 255), 1)
        output_movie.write(frame)
        cv2.imwrite("media/exam/more_than_1/"+current_frame+".jpg", frame)
    if len(detected_faces) == 1:
        #face_detection_list.append(1)
        frames_list.append(current_frame)
        #Find facial landmarks in the detected face
        landmarks = pose_predictor(frame, detected_faces[0])
        list_of_landmarks = [(part.x,part.y) for part in landmarks.parts()] #list contains all 68 landmarks
        
        #Find the 128 face encodings of examinee face
        face_descriptor = np.array(facerec.compute_face_descriptor(frame, landmarks))
        #print face_descriptor

        end_time = timeit.default_timer()
        #print end_time - start_time

        #Calculate euclidean distance
        euclidean_distance = np.linalg.norm(np.array(pre_encoding)-np.array(face_descriptor))
        print "Distance = ", euclidean_distance

        if euclidean_distance <= 0.5:
            name = "Examinee"
            print "Examinee FACE"
            cv2.putText(frame, "Examinee Face Detected", (15 +20, 15 + 20), font, 0.5, (255, 255, 255), 1)
        else:
            name="Unknown"
            print "Unknown FACE"
            cv2.putText(frame, "Unknown Face Detected", (15 +20, 15 + 20), font, 0.5, (255, 255, 255), 1)

        face_names = []
        face_names.append(name)

    # Label the results

        # Draw a box around the face
        cv2.rectangle(frame, (detected_faces[0].left(), detected_faces[0].top()), (detected_faces[0].right(), detected_faces[0].bottom()), (255, 255, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (detected_faces[0].left(), detected_faces[0].bottom() - 25), (detected_faces[0].right(), detected_faces[0].bottom()), (0, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (detected_faces[0].left() + 6, detected_faces[0].bottom() - 6), font, 0.5, (255, 255, 255), 1)
      
        # Write the resulting image to the output video file
        output_movie.write(frame)

    #frame set
    frame_number += fps

print duration
#Saving duration to a file
save = open('database/duration.dat', 'wb')
pickle.dump(duration, save)

input_movie.release()
cv2.destroyAllWindows()
        

plt.title("Face presence/disapperence") 
plt.xlabel("Frames") 
plt.ylabel("") 
ax = plt.axes()
ax.yaxis.set_major_locator(plt.FixedLocator([0,1]))
ax.yaxis.set_major_formatter(plt.FixedFormatter(['Not Present', 'Present']))
plt.plot(frames_list,face_detection_list) 
plt.show()
    
    



