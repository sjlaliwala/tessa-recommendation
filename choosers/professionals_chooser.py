from choosers.chooser import Chooser
from models.tag_similarity import *
import random

PROFESSIONALS_LIMIT = 2
TOP_N_LIMIT = 10

class ProfessionalsChooser(Chooser):

  def __init__(self, professionals, user_interests, past_user_professionals):
    self.professionals = professionals
    self.user_interests = user_interests
    self.past_user_professionals = set(past_user_professionals)

  def choose(self):
    most_similar_professionals = self.calculate_most_similar_professionals()
    top_n_most_similar_professionals = most_similar_professionals[0: self.decide_n(most_similar_professionals)]
    most_similar_professionals = random.sample(top_n_most_similar_professionals, PROFESSIONALS_LIMIT)
    self.add_labeled_tags_in_common(most_similar_professionals)
    return most_similar_professionals

  def decide_n(self, most_similar_professionals):
    return TOP_N_LIMIT if len(most_similar_professionals) >= TOP_N_LIMIT else len(most_similar_professionals)

  def calculate_most_similar_professionals(self):
    most_similar_professionals = []
    user_interests_tags = self.get_user_interest_tags()
    for professional_id, professional in self.professionals.items():
      if professional_id not in self.past_user_professionals:
        professional_interests = self.get_professional_interest_tags(professional)
        similarity = calculate_jaccard_similarity(user_interests_tags, professional_interests)
        most_similar_professionals.append({**professional, 'professional_id': professional_id, 'similarity': similarity})

    most_similar_professionals = sorted(most_similar_professionals, key=lambda p: p['similarity'], reverse=True)
    return most_similar_professionals

  def add_labeled_tags_in_common(self, most_similar_professionals):
    user_interests = self.get_user_interest_tags()
    for professional in most_similar_professionals:
      labeled_tags_in_common = {}
      professional_interests = self.get_professional_interest_tags(professional)
      tags_in_common = user_interests.intersection(professional_interests)
      for label, tags in self.user_interests.items():
        filtered_tags = list(filter(lambda tag: tag in tags_in_common, tags))
        labeled_tags_in_common[label] = filtered_tags
      professional['tags_in_common'] = labeled_tags_in_common
      
  def get_user_interest_tags(self):
    user_interests = set(interest.lower() for interest_group in self.user_interests.values() for interest in interest_group)
    return user_interests

  def get_professional_interest_tags(self, professional):
    professional_interests = set(tag.lower() for tag in professional['tags'])
    return professional_interests

    






      


  


    

    


