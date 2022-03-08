import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import NEWS_RECOMMENDATIONS

class NewsRecommendationsDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.news_recommendations = local_db.load_table(NEWS_RECOMMENDATIONS)

  def get_all_news_recommendations(self):
    if self.news_recommendations == None:
      news_recommendations = {}
      docs = self.db.collection(NEWS_RECOMMENDATIONS).stream()
      for doc in docs:
        news_rec_data = doc.to_dict()
        uid = news_rec_data['uid']
        if uid not in news_recommendations:
          news_recommendations[uid] = []
        articles_ids = [article['article_id'] for article in news_rec_data['news']]
        news_recommendations[uid].extend(articles_ids)
      local_db.cache_table(NEWS_RECOMMENDATIONS, news_recommendations)
      self.news_recommendations = news_recommendations
    return self.news_recommendations
        


  