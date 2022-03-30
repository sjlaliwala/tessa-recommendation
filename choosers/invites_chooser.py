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
    professional_career = self.recommended_professional['career'].lower()
    professional_domain = self.recommended_professional['domain'].lower()
    if self.user_data['school'] != '' and self.user_data['major'] != '' and random.choice([True, False]):
      user_major = self.user_data['major'].lower()
      user_school = self.user_data['school']
      return NETWORKING_INVITE_TEMPLATE.format(professional_first_name, f'{user_major} major', user_school, professional_career, professional_domain)
    else:
      user_career = self.user_data['position'].lower()
      user_company = self.user_data['company']
      return NETWORKING_INVITE_TEMPLATE.format(professional_first_name, user_career, user_company, professional_career, professional_domain)