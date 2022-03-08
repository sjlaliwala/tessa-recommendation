from dao.news_dao import NewsDao
from recommendations.recommendations import Recommendations
from dao.news_recommendations_dao import NewsRecommendationsDao
from dao.users_dao import UsersDao
from choosers.news_chooser import NewsChooser

class NewsRecommendations(Recommendations):

  def __init__(self, daos, recommendation_timestamp_str):
    self.user_dao: UsersDao = daos['users']
    self.news_dao: NewsDao = daos['news']
    self.recommendations_dao: NewsRecommendationsDao = daos['news_recommendations']
    self.recommendation_timestamp_str = recommendation_timestamp_str
    self.recommendations = None

  def extract(self):
    users = self.user_dao.get_all_users()
    news = self.news_dao.get_all_news()
    news_recommendations = self.recommendations_dao.get_all_news_recommendations()
    return users, news, news_recommendations

  def transform(self, users, news, news_recommendations):
    user_news_recommendations = {}
    for user_id, user_data in users.items():
      user_news_interests = user_data['domains']
      past_user_news = news_recommendations[user_id] if user_id in news_recommendations else []
      news_chooser = NewsChooser(news, user_news_interests, past_user_news)
      recommended_news = news_chooser.choose()
      user_news_recommendations[user_id + self.recommendation_timestamp_str] = recommended_news
    return user_news_recommendations
    
  def load(self, user_news_recommendations):
    pass

  def generate(self):
    users, news, news_recommendations = self.extract()
    user_news_recommendations = self.transform(users, news, news_recommendations)
    print('news: ', user_news_recommendations)
    self.load(user_news_recommendations)