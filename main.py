from dao.daos import Daos
import time
from recommendations.recommendations import Recommendations
from recommendations.news_recommendations import NewsRecommendations
from recommendations.professionals_recommendations import ProfessionalsRecommendations
from loaders.recommendation_loader import RecommendationLoader


def main():
  daos = Daos().get_daos()
  recommendation_generators: list[Recommendations] = [
    NewsRecommendations(daos),
    ProfessionalsRecommendations(daos)
  ]
  recommendations = [rec.generate() for rec in recommendation_generators]
  recommendation_timestamp = int(time.time() * 1000)
  recommendation_loader = RecommendationLoader(recommendations, recommendation_timestamp)
  recommendation_loader.load()
  
  
  
if __name__ == "__main__":
  main()