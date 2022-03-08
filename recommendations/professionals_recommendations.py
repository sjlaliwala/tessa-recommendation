from choosers.professionals_chooser import ProfessionalsChooser
from dao.professionals_recommendations_dao import ProfessionalsRecommendationsDao
from dao.professionals_dao import ProfessionalsDao
from dao.users_dao import UsersDao
from recommendations.recommendations import Recommendations

class ProfessionalsRecommendations(Recommendations):

  def __init__(self, daos, recommendation_timestamp_str):
    self.users_dao: UsersDao = daos['users']
    self.professionals_dao: ProfessionalsDao = daos['professionals']
    self.professionals_recommendations_dao: ProfessionalsRecommendationsDao = daos['professionals_recommendations']
    self.recommendation_timestamp_str = recommendation_timestamp_str

  def extract(self):
    users = self.users_dao.get_all_users()
    professionals = self.professionals_dao.get_all_professionals()
    professionals_recommendations = self.professionals_recommendations_dao.get_all_professional_recommendations()
    return users, professionals, professionals_recommendations

  def transform(self, users, professionals, professionals_recommendations):
    user_professional_recommendations = {}
    for user_id, user_data in users.items():
      user_professionals_interests = user_data['careers'] + user_data['domains'] + user_data['locations']
      past_user_professionals = professionals_recommendations[user_id] if user_id in professionals_recommendations else []
      professionals_chooser = ProfessionalsChooser(professionals, user_professionals_interests, past_user_professionals)
      recommended_professionals = professionals_chooser.choose()
      user_professional_recommendations[user_id + self.recommendation_timestamp_str] = recommended_professionals
      return user_professional_recommendations

  def load(self, user_professional_recommendations):
    pass

  def generate(self):
    users, professionals, professionals_recommendations = self.extract()
    user_professional_recommendations = self.transform(users, professionals, professionals_recommendations)
    print('professionals: ', user_professional_recommendations)
    self.load(user_professional_recommendations)
