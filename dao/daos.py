from dao.news_dao import NewsDao
from dao.professionals_dao import ProfessionalsDao
from dao.users_dao import UsersDao
from dao.recommendations_dao import RecommendationsDao

daos = {
  'users': UsersDao(),
  'news': NewsDao(),
  'professionals': ProfessionalsDao(),
  'recommendations': RecommendationsDao()
}