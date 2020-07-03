import dlib
import numpy as np
from PIL import Image, ImageDraw
import pickle


examinee_name = "Mohammed"
examinee_face_encodings = {}

#Load the image from the disk
examinee_image = np.array(Image.open('./media/training/examinee_image.jpeg').convert("RGB"))
#'./media/training/Mohamed/image_out1.png'
#'./media/training/examinee_image.jpeg'

#Load the pose predictor model
predictor_model = "models/shape_predictor_68_face_landmarks.dat"
pose_predictor = dlib.shape_predictor(predictor_model)

#Load the face detector model
face_detector = dlib.get_frontal_face_detector()

#Load the face recognition trained model
rec_model = "models/dlib_face_recognition_resnet_model_v1.dat"
facerec = dlib.face_recognition_model_v1(rec_model)

#Find faces in the image
detected_faces = face_detector(examinee_image, 1) #Rectangle object with top(), bottom, left,right
#print detected_faces[0].top() 

if len(detected_faces) > 1:
    print "there are more than one examinee"
    exit()


#Find facial landmarks in the detected faces
landmarks = pose_predictor(examinee_image, detected_faces[0])
list_of_landmarks = [(part.x,part.y) for part in landmarks.parts()] #list contains all 68 landmarks
print len(list_of_landmarks)

#Find the 128 face encodings of examinee face
face_descriptor = list(facerec.compute_face_descriptor(examinee_image, landmarks))
#print face_descriptor


examinee_face_encodings[examinee_name] = face_descriptor

#Saving face encoding to a file
save = open('database/examinee_face_encodings.dat', 'wb')
pickle.dump(examinee_face_encodings, save)

""" # Let's trace out each facial feature in the image with a line!
pil_image = Image.fromarray(examinee_image)
d = ImageDraw.Draw(pil_image)

for face in list_of_landmarks:
    d.point(face, fill="white")

pil_image.show() """