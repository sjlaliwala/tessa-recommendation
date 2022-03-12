from choosers.chooser import Chooser
import random

NEWS_ARTICLE_LIMIT = 2

class NewsChooser(Chooser):
  def __init__(self, news, user_news_interests, past_user_news):
    self.news = news
    self.past_user_news = set(past_user_news)
    self.user_news_interests = set(user_news_interests)
    self.topics_to_fetch = []

  def choose(self):
    news_topics = self.get_news_topics()
    news_articles = self.get_news_articles(news_topics)
    return news_articles

  def get_news_topics(self):
    news_topics = []
    for i in range(NEWS_ARTICLE_LIMIT):
      topic = None
      while topic not in self.news:
        topic = random.choice(list(self.user_news_interests))
        if topic not in self.news:
          self.user_news_interests.remove(topic)
          self.topics_to_fetch.append(topic)
          print(f'YOU NEED TO FETCH MORE {topic} news')
      news_topics.append(topic)
    return news_topics

  def get_news_articles(self, news_topics):
    news_articles = []
    seen_articles = set()
    for topic in news_topics:
      news_by_topic = self.news[topic]
      article_id = None
      while article_id is None or article_id in seen_articles or article_id in self.past_user_news:
        article_id = random.choice(list(news_by_topic.keys()))
      seen_articles.add(article_id)
      news_articles.append({**news_by_topic[article_id], 'article_id': article_id})
    return news_articles
      

      
      
