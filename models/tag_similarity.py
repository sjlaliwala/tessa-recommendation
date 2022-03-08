def calculate_jaccard_similarity(a: set, b: set):
  jaccard_similarity = float(len(a.intersection(b))) / len(a.union(b))
  return jaccard_similarity

def calculate_intersection_similarity(a: set, b: set):
  intersection_similarity = float(len(a.intersection(b))) / len(b)
  return intersection_similarity