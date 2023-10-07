from choosers.invites_chooser import InvitesChooser
from choosers.professionals_chooser import ProfessionalsChooser
from config.table_names import PROFESSIONALS, RECOMMENDATIONS, USERS
from dao.professionals_dao import ProfessionalsDao
from dao.recommendations_dao import RecommendationsDao
from dao.users_dao import UsersDao
from recommendations.recommendations import Recommendations


class ProfessionalsRecommendations(Recommendations):

  def __init__(self, daos):
    self.users_dao: UsersDao = daos[USERS]
    self.professionals_dao: ProfessionalsDao = daos[PROFESSIONALS]
    self.recommendations_dao: RecommendationsDao = daos[RECOMMENDATIONS]
    self.type = PROFESSIONALS

  def extract(self):
    users = self.users_dao.get_all_users()
    professionals = self.professionals_dao.get_all_professionals()
    past_recommendations = self.recommendations_dao.get_all_past_recommendations()
    return users, professionals, past_recommendations

  def transform(self, users, professionals, past_recommendations):
    professional_recommendations = {}
    for user_id, user_data in users.items():
      user_interests = user_data['interests'] if user_data['onboarded'] else {}
      recommended_professionals = self.generate_recommended_professionals(user_id, user_interests, professionals, past_recommendations)
      self.add_in_recommended_invites(user_data, recommended_professionals)
      professional_recommendations[user_id] = recommended_professionals
    return professional_recommendations

  def generate_recommended_professionals(self, user_id, user_interests, professionals, past_recommendations):
    past_user_professionals = past_recommendations[user_id]['professionals'] if user_id in past_recommendations and 'professionals' in past_recommendations[user_id] else []
    professionals_chooser = ProfessionalsChooser(professionals, user_interests, past_user_professionals)
    recommended_professionals = professionals_chooser.choose()
    return recommended_professionals
  
  def add_in_recommended_invites(self, user_data, recommended_professionals):
    for professional in recommended_professionals:
      invites_chooser = InvitesChooser(user_data, professional)
      recommended_invite = invites_chooser.choose()
      professional['invite'] = recommended_invite

  def generate(self):
    users, professionals, professionals_recommendations = self.extract()
    professional_recommendations = self.transform(users, professionals, professionals_recommendations)
    return self.type, professional_recommendations
