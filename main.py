from dao.daos import daos
import time
from recommendations.news_recommendations import NewsRecommendations
from recommendations.professionals_recommendations import ProfessionalsRecommendations

def main():
  recommendation_date = {'timestamp': int(time.time() * 1000), 'date': '03-12-2022'}
  news_recommendations = NewsRecommendations(daos, recommendation_date)
  news_recommendations.generate()
  professionals_recommendations = ProfessionalsRecommendations(daos, recommendation_date)
  professionals_recommendations.generate()


if __name__ == "__main__":
  main()