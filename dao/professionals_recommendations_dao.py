import connectors.firebase_connector as firebase
import local_db.local_db_manager as local_db
from config.table_names import PROFESSIONALS_RECOMMENDATIONS
from itertools import islice

BATCH_SIZE = 500

class ProfessionalsRecommendationsDao():

  def __init__(self):
    self.db = firebase.get_firestore_client()
    self.batch = self.db.batch()
    self.professionals_recomendations = local_db.load_table(PROFESSIONALS_RECOMMENDATIONS)

  def get_all_professional_recommendations(self):
    if self.professionals_recomendations == None:
      professionals_recommendations = {}
      docs = self.db.collection(PROFESSIONALS_RECOMMENDATIONS).stream()
      for doc in docs:
        prof_rec_data = doc.to_dict()
        uid = prof_rec_data['uid']
        if uid not in professionals_recommendations:
          professionals_recommendations[uid] = []
        professional_ids = [p['professional_id'] for p in prof_rec_data['professionals']]
        professionals_recommendations[uid].extend(professional_ids)
      local_db.cache_table(PROFESSIONALS_RECOMMENDATIONS, professionals_recommendations)
      self.professionals_recomendations = professionals_recommendations
    return self.professionals_recomendations

  def add_professionals_recommendations(self, professionals_recommendations):
    for professionals_recommendation_batch in self.chunks(professionals_recommendations):
      for professionals_recommendation_id, professionals_recommendation in professionals_recommendation_batch.items():
        professionals_recommendation_ref = self.db.collection(PROFESSIONALS_RECOMMENDATIONS).document(professionals_recommendation_id)
        self.batch.set(professionals_recommendation_ref, professionals_recommendation)
      self.batch.commit()

  def chunks(self, data, size=BATCH_SIZE):
    it = iter(data)
    for i in range(0, len(data), size):
      yield {k:data[k] for k in islice(it, size)}
