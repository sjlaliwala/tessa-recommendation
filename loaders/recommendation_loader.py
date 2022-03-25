from dao.recommendations_dao import RecommendationsDao

class RecommendationLoader():

  def __init__(self, typed_recommendations, recommendation_timestamp):
    self.typed_recommendations = typed_recommendations
    self.timestamp = recommendation_timestamp
    self.recommendations_dao = RecommendationsDao()

  def load(self):
    aggregated_recommendations = self.aggregate()
    self.recommendations_dao.add_recommendations(aggregated_recommendations)

  def aggregate(self):
    aggregated_recommendations = {}
    for type, recommendations in self.typed_recommendations:
      for uid, recommendation in recommendations.items():
        user_recommendation_key = f'{uid}#{self.timestamp}'
        if user_recommendation_key not in aggregated_recommendations:
          aggregated_recommendations[user_recommendation_key] = {
            'uid': uid,
            'timestamp': self.timestamp,
          }
        aggregated_recommendations[user_recommendation_key][type] = recommendation
    return aggregated_recommendations


