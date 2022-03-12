from abc import ABC, abstractmethod

class Recommendations(ABC):
  batch_size = 500

  @abstractmethod
  def extract():
    pass

  @abstractmethod
  def transform():
    pass

  @abstractmethod
  def load():
    pass

  @abstractmethod
  def generate():
    pass
