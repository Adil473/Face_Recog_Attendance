
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://faceattendance-e4d4b-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {

    "146":{
    "name" : "Aarya Redekar",
    "Branch" : "COMPS",
    "Year" : "TE",
    "total_attendance" : 2,
    "Class" : "C3",
    "last_attendance_time" : "2023-04-03 18:06:17"
    },


    "150":{
    "name" : "Soham Sanghvi",
    "Branch" : "COMPS",
    "Year" : "TE",
    "total_attendance" : 1,
    "Class" : "C3",
    "last_attendance_time" : "2023-04-03 18:06:17"
    }
}

for key,value in data.items():
    ref.child(key).set(value)