from choosers.chooser import Chooser
from templates.invites import *
import random

INVITE_PROBABILITY = .5
class InvitesChooser(Chooser):

  def __init__(self, user_data, recommended_professional):
    self.user_data = user_data
    self.recommended_professional = recommended_professional
  
  def choose(self):
    recommended_invite = self.format_invite()
    return recommended_invite

  def format_invite(self):
    professional_first_name = self.recommended_professional['name'].split(' ')[0]
    professional_career = self.default_if_empty(self.recommended_professional['career'].lower() if 'career' in self.recommended_professional else '', 'ADD_PROFESSIONAL\'S_CAREER')
    professional_domain = self.default_if_empty(self.recommended_professional['domain'].lower() if 'domain' in self.recommended_professional else '', 'ADD_PROFESSIONAL\'S_INTEREST')
    if 'school' in self.user_data and 'major' in self.user_data and random.choice([True, False]):
      user_major = self.default_if_empty(self.user_data['major'].lower() if 'major' in self.user_data else '', 'ADD_MAJOR')
      user_school = self.default_if_empty(self.user_data['school'] if 'school' in self.user_data else '', 'ADD_SCHOOL')
      return NETWORKING_INVITE_TEMPLATE.format(professional_first_name, f'{user_major} major', user_school, professional_career, professional_domain)
    else:
      user_career = self.default_if_empty(self.user_data['position'].lower() if 'position' in self.user_data else '', 'ADD_POSITION')
      user_company = self.default_if_empty(self.user_data['company'] if 'company' in self.user_data else '', 'ADD_COMPANY/ORGANIZATION')
      return NETWORKING_INVITE_TEMPLATE.format(professional_first_name, user_career, user_company, professional_career, professional_domain)

  def default_if_empty(self, value, default_value):
    return default_value if value is None or len(value) == 0 else value
    
