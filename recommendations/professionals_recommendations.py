from choosers.invites_chooser import InvitesChooser
from choosers.professionals_chooser import ProfessionalsChooser
from dao.professionals_recommendations_dao import ProfessionalsRecommendationsDao
from dao.professionals_dao import ProfessionalsDao
from dao.users_dao import UsersDao
from recommendations.recommendations import Recommendations

class ProfessionalsRecommendations(Recommendations):

  def __init__(self, daos, recommendation_date):
    self.users_dao: UsersDao = daos['users']
    self.professionals_dao: ProfessionalsDao = daos['professionals']
    self.professionals_recommendations_dao: ProfessionalsRecommendationsDao = daos['professionals_recommendations']
    self.recommendation_timestamp = recommendation_date['timestamp']
    self.recommendation_date = recommendation_date['date']

  def extract(self):
    users = self.users_dao.get_all_users()
    professionals = self.professionals_dao.get_all_professionals()
    professionals_recommendations = self.professionals_recommendations_dao.get_all_professional_recommendations()
    return users, professionals, professionals_recommendations

  def transform(self, users, professionals, professionals_recommendations):
    professional_recommendations = {}
    for user_id, user_data in users.items():
      recommended_professionals = self.generate_recommended_professionals(user_id, user_data['interests'], professionals, professionals_recommendations)
      self.add_in_recommended_invites(user_data, recommended_professionals)
      professional_recommendations[f'{user_id}#{self.recommendation_date}'] = {
        'uid': user_id, 
        'timestamp': self.recommendation_timestamp,
        'date': self.recommendation_date,
        'professionals': recommended_professionals
      }
      return professional_recommendations

  def generate_recommended_professionals(self, user_id, user_interests, professionals, professionals_recommendations):
      past_user_professionals = professionals_recommendations[user_id] if user_id in professionals_recommendations else []
      professionals_chooser = ProfessionalsChooser(professionals, user_interests, past_user_professionals)
      recommended_professionals = professionals_chooser.choose()
      return recommended_professionals
  
  def add_in_recommended_invites(self, user_data, recommended_professionals):
    for professional in recommended_professionals:
      invites_chooser = InvitesChooser(user_data, professional)
      recommended_invite = invites_chooser.choose()
      professional['invite'] = recommended_invite

  def load(self,professional_recommendations):
    self.professionals_recommendations_dao.add_professionals_recommendations(professional_recommendations)

  def generate(self):
    users, professionals, professionals_recommendations = self.extract()
    professional_recommendations = self.transform(users, professionals, professionals_recommendations)
    self.load(professional_recommendations)
