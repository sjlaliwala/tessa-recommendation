import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import NEWS

class NewsDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.news = local_db.load_table(NEWS)

  def get_all_news(self):
    if self.news == None:
      news = {}
      docs = self.db.collection(NEWS).stream()
      for doc in docs:
        article_id = doc.id
        article = doc.to_dict()
        topic = article['topic']
        if topic not in news:
          news[topic] = {}
        news[topic][article_id] = article
      local_db.cache_table(NEWS, news)
      self.news = news
    return self.news

