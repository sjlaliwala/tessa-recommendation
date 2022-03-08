import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import USERS

class UsersDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.users = local_db.load_table(USERS)

  def get_all_users(self):
    if self.users == None:
      users = {}
      docs = self.db.collection(USERS).stream()
      for doc in docs:
        users[doc.id] = doc.to_dict()
      local_db.cache_table(USERS, users)
      self.users = users
    return self.users

