import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import TEST_USERS

class TestUsersDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.users = local_db.load_table(TEST_USERS)

  def get_all_users(self):
    return self.users

