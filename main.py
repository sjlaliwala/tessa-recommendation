from dao.daos import daos
from datetime import datetime
import pytz
from recommendations.news_recommendations import NewsRecommendations
from recommendations.professionals_recommendations import ProfessionalsRecommendations

def main():
  recommendation_timestamp_str = datetime(2022, 3, 7, 13, 0, 0).strftime('%Y-%m-%d %H:%M:%S')
  news_recommendations = NewsRecommendations(daos, recommendation_timestamp_str)
  news_recommendations.generate()
  professionals_recommendations = ProfessionalsRecommendations(daos, recommendation_timestamp_str)
  professionals_recommendations.generate()

  

  
  



if __name__ == "__main__":
  main()