from dao.news_dao import NewsDao
from dao.professionals_dao import ProfessionalsDao
from dao.users_dao import UsersDao
from dao.recommendations_dao import RecommendationsDao
from dao.test_users_dao import TestUsersDao

class Daos():
  def __init__(self, dev=False):
    self.daos = {
        'news': NewsDao(),
        'professionals': ProfessionalsDao(),
        'recommendations': RecommendationsDao()
      }
    if dev:
      self.daos['users'] = TestUsersDao()
    else:
      self.daos['users'] = UsersDao()

  def get_daos(self):
    return self.daos