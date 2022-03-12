from dao.news_dao import NewsDao
from recommendations.recommendations import Recommendations
from dao.news_recommendations_dao import NewsRecommendationsDao
from dao.users_dao import UsersDao
from choosers.news_chooser import NewsChooser

class NewsRecommendations(Recommendations):

  def __init__(self, daos, recommendation_date):
    self.user_dao: UsersDao = daos['users']
    self.news_dao: NewsDao = daos['news']
    self.news_recommendations_dao: NewsRecommendationsDao = daos['news_recommendations']
    self.recommendation_timestamp = recommendation_date['timestamp']
    self.recommendation_date = recommendation_date['date']

  def extract(self):
    users = self.user_dao.get_all_users()
    news = self.news_dao.get_all_news()
    prev_news_recommendations = self.news_recommendations_dao.get_all_news_recommendations()
    return users, news, prev_news_recommendations

  def transform(self, users, news, prev_news_recommendations):
    news_recommendations = {}
    for user_id, user_data in users.items():
      user_news_interests = user_data['interests']['domains']
      past_user_news = prev_news_recommendations[user_id] if user_id in prev_news_recommendations else []
      news_chooser = NewsChooser(news, user_news_interests, past_user_news)
      recommended_news = news_chooser.choose()
      news_recommendations[f'{user_id}#{self.recommendation_date}'] = {
        'uid': user_id,
        'timestamp': self.recommendation_timestamp,
        'date': self.recommendation_date,
        'news': recommended_news
      }
    return news_recommendations
    
  def load(self, news_recommendations):
    self.news_recommendations_dao.add_news_recommendations(news_recommendations)

  def generate(self):
    users, news, prev_news_recommendations = self.extract()
    news_recommendations = self.transform(users, news, prev_news_recommendations)
    self.load(news_recommendations)