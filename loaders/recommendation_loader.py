from dao.recommendations_dao import RecommendationsDao

class RecommendationLoader():

  def __init__(self, typed_recommendations, recommendation_date):
    self.typed_recommendations = typed_recommendations
    self.timestamp = recommendation_date['timestamp']
    self.date = recommendation_date['date']
    self.recommendations_dao = RecommendationsDao()

  def load(self):
    aggregated_recommendations = self.aggregate()
    self.recommendations_dao.add_recommendations(aggregated_recommendations)

  def aggregate(self):
    aggregated_recommendations = {}
    for type, recommendations in self.typed_recommendations:
      for uid, recommendation in recommendations.items():
        user_recommendation_key = f'{uid}#{self.date}'
        if user_recommendation_key not in aggregated_recommendations:
          aggregated_recommendations[user_recommendation_key] = {
            'uid': uid,
            'timestamp': self.timestamp,
            'date': self.date
          }
        aggregated_recommendations[f'{uid}#{self.date}'][type] = recommendation
    return aggregated_recommendations


