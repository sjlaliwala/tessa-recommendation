import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import NEWS_RECOMMENDATIONS
from itertools import islice

BATCH_SIZE = 500

class NewsRecommendationsDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.batch = self.db.batch()
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

  def add_news_recommendations(self, news_recommendations):
    for news_recommendation_batch in self.chunks(news_recommendations):
      for news_recommendation_id, news_recommendation in news_recommendation_batch.items():
        news_recommendation_ref = self.db.collection(NEWS_RECOMMENDATIONS).document(news_recommendation_id)
        self.batch.set(news_recommendation_ref, news_recommendation)
      self.batch.commit()

  def chunks(self, data, size=BATCH_SIZE):
    it = iter(data)
    for i in range(0, len(data), size):
      yield {k:data[k] for k in islice(it, size)}

        


  