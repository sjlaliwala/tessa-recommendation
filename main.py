from dao.daos import daos
import time
from recommendations.recommendations import Recommendations
from recommendations.news_recommendations import NewsRecommendations
from recommendations.professionals_recommendations import ProfessionalsRecommendations
from loaders.recommendation_loader import RecommendationLoader


def main():
  recommendation_generators: list[Recommendations] = [
    NewsRecommendations(daos),
    ProfessionalsRecommendations(daos)
  ]
  recommendations = [rec.generate() for rec in recommendation_generators]
  recommendation_date = {'timestamp': int(time.time() * 1000), 'date': '03-13-2022'}
  recommendation_loader = RecommendationLoader(recommendations, recommendation_date)
  recommendation_loader.load()
  
  
  
if __name__ == "__main__":
  main()