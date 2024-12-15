import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, auth
import socket
from random import randint

class Database:
 def __init__(self):
     self.firebase_instance = self.create_firebase_app()
     db = firestore.client()
     self.clients = db.collection("clients")
     self.my_id = None

 def create_firebase_app(self):
     cred = credentials.Certificate("../cred.json")
     firebase = firebase_admin.initialize_app(cred)
     return firebase
 
 def signUp(self, username, email, password):
     try:
        auth.create_user(email=email, email_verified=True,password=password, display_name=username)
        clientId = self.signIn(username, email)[1].split("#")[3]
        return True, 'SignUp#OK#{username} created successfully#'+ clientId
     except Exception as e:
        return False, 'SignUp#ERROR#{username} already exist'
 
 def signIn(self, username, email):
     try:
         user = auth.get_user_by_email(email)
         if not username:
             res = self.clients.document(user.uid).get().to_dict()
             self.username = res["username"]
         else:
             self.username = username
         self.my_id = user.uid
         clientId = self.update_user("On")
         return True, 'SignIn#OK#sign in successfully#' + clientId
     except Exception as e:
         return False, 'SignIn#ERROR#Client not found'


 def get_data(self, id):
     doc_ref = self.clients.document(id)
     data = doc_ref.get().to_dict()
     return data







