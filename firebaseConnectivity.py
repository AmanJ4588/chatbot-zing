import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import db

cred = credentials.Certificate("C:\Users\Aman\Downloads\chatbot-zing-e77df-firebase-adminsdk-nelvr-66994cf765.json")
firebase_admin.initialize_app(cred)
