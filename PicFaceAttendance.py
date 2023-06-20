import face_recognition
import pickle
from PIL import Image
import pybind11

file = open('EncodeFile.p', 'rb')
encodeListKnownWithIDS = pickle.load(file)
file.close()
encodeListKnown, StudentIds = encodeListKnownWithIDS

known_image = face_recognition.load_image_file("group2.jpg")
#unknown_image = face_recognition.load_image_file("3.png")
face_loc = face_recognition.face_locations(known_image)

List_encoding = face_recognition.face_encodings(known_image)
print(len(List_encoding))

#Adil_encoding = face_recognition.face_encodings(known_image)[1]
#unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
for i in range(len(List_encoding)):
    top, right, bottom, left = face_loc[i]
    results = face_recognition.compare_faces(List_encoding[i], encodeListKnown)
    print(results)
    for j in range(len(results)):
        if results[j] == True:
            print(StudentIds[j])
            face_image = known_image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.show()
