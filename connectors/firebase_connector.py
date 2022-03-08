import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from config.config import CONFIG

cred = credentials.Certificate(CONFIG['firebase_config'])
firebase_admin.initialize_app(cred, {
  'projectId': CONFIG['firebase_project'],
})

def get_firestore_client():
  return firestore.client()