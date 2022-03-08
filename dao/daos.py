from dao.news_dao import NewsDao
from dao.news_recommendations_dao import NewsRecommendationsDao
from dao.professionals_dao import ProfessionalsDao
from dao.professionals_recommendations_dao import ProfessionalsRecommendationsDao
from dao.users_dao import UsersDao

daos = {
  'users': UsersDao(),
  'news': NewsDao(),
  'news_recommendations': NewsRecommendationsDao(),
  'professionals': ProfessionalsDao(),
  'professionals_recommendations': ProfessionalsRecommendationsDao()
}