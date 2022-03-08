from abc import ABC, abstractmethod

class Chooser(ABC):

  @abstractmethod
  def choose(self):
    pass