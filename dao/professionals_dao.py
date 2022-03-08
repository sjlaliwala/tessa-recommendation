import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import PROFESSIONALS

class ProfessionalsDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.professionals = local_db.load_table(PROFESSIONALS)

  def get_all_professionals(self):
    if self.professionals == None:
      professionals = {}
      docs = self.db.collection(PROFESSIONALS).stream()
      for doc in docs:
        professionals[doc.id] = doc.to_dict()
      local_db.cache_table(PROFESSIONALS, professionals)
      self.professionals= professionals
    return self.professionals
