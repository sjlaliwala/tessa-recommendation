import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import PROFESSIONALS_RECOMMENDATIONS, RECOMMENDATIONS
from itertools import islice

BATCH_SIZE = 500

def is_recommendation_key(key): 
  return key not in {'timestamp', 'date', 'uid'}

class RecommendationsDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.batch = self.db.batch()
    self.recomendations = local_db.load_table(RECOMMENDATIONS)

  def get_all_past_recommendations(self):
    if self.recomendations == None:
      recommendations = {}
      docs = self.db.collection(RECOMMENDATIONS).stream()
      for doc in docs:
        rec_data = doc.to_dict()
        uid = rec_data['uid']
        if uid not in recommendations:
          recommendations[uid] = {}
        for key, data in rec_data.items():
          if is_recommendation_key(key):
            if key not in recommendations[uid]:
              recommendations[uid][key] = []
            recommendations[uid][key].extend([d['id'] for d in data])     
      local_db.cache_table(RECOMMENDATIONS, recommendations)
      self.recomendations = recommendations
    return self.recomendations

  def add_recommendations(self, recommendations):
    for recommendations_batch in self.chunks(recommendations):
      for recommendation_id, recommendation in recommendations_batch.items():
        recommendation_ref = self.db.collection(RECOMMENDATIONS).document(recommendation_id)
        self.batch.set(recommendation_ref, recommendation)
      self.batch.commit()

  def chunks(self, data, size=BATCH_SIZE):
    it = iter(data)
    for i in range(0, len(data), size):
      yield {k:data[k] for k in islice(it, size)}
