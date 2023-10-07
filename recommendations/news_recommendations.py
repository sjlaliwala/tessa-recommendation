from config.table_names import NEWS, RECOMMENDATIONS, USERS
from dao.news_dao import NewsDao
from dao.recommendations_dao import RecommendationsDao
from recommendations.recommendations import Recommendations
from dao.users_dao import UsersDao
from choosers.news_chooser import NewsChooser

class NewsRecommendations(Recommendations):

  def __init__(self, daos):
    self.user_dao: UsersDao = daos[USERS]
    self.news_dao: NewsDao = daos[NEWS]
    self.recommendations_dao: RecommendationsDao = daos[RECOMMENDATIONS]
    self.type = NEWS

  def extract(self):
    users = self.user_dao.get_all_users()
    news = self.news_dao.get_all_news()
    past_recommendations = self.recommendations_dao.get_all_past_recommendations()
    return users, news, past_recommendations

  def transform(self, users, news, past_recommendations):
    news_recommendations = {}
    for user_id, user_data in users.items():
      user_news_interests = user_data['interests']['domains'] if user_data['onboarded'] else []
      past_user_news = past_recommendations[user_id]['news'] if user_id in past_recommendations and 'news' in past_recommendations[user_id] else []
      news_chooser = NewsChooser(news, user_news_interests, past_user_news)
      recommended_news = news_chooser.choose()
      news_recommendations[user_id] = recommended_news
    return news_recommendations

  def generate(self):
    users, news, past_news_recommendations = self.extract()
    news_recommendations = self.transform(users, news, past_news_recommendations)
    return self.type, news_recommendations