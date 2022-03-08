from choosers.chooser import Chooser
from models.tag_similarity import *

PROFESSIONALS_LIMIT = 2

class ProfessionalsChooser(Chooser):

  def __init__(self, professionals, user_professionals_interests, past_user_professionals):
    self.professionals = professionals
    self.user_professionals_interests = set(interest.lower() for interest in user_professionals_interests)
    self.past_user_professionals = set(past_user_professionals)

  def choose(self):
    most_similar_professionals = self.calculate_most_similar_professionals()
    return most_similar_professionals[0:PROFESSIONALS_LIMIT]

  def calculate_most_similar_professionals(self):
    most_similar_professionals = []
    for professional_id, professional in self.professionals.items():
      if professional_id not in self.past_user_professionals:
        professional_interests = set(tag.lower() for tag in professional['tags'])
        similarity = calculate_jaccard_similarity(self.user_professionals_interests, professional_interests)
        most_similar_professionals.append({**professional, 'professional_id': professional_id, 'similarity': similarity})

    most_similar_professionals = sorted(most_similar_professionals, key=lambda p: p['similarity'], reverse=True)
    return most_similar_professionals


      


  


    

    


