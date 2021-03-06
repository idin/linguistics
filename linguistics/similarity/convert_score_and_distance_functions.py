from editdistance import eval as get_edit_distance
from jellyfish import jaro_winkler as get_similarity

def convert_distance_function_to_score_function(function=get_edit_distance):
	def score_func(s1, s2):
		distance = function(s1, s2)
		score = max(0,1-float(distance)/max(len(s1), len(s2)))
		return score
	return score_func

def create_weighted_similarity_function(function=get_similarity, first_letter_weight=1):
	def new_score_func(s1, s2):
		original_result = function(s1, s2)
		first_letter_result = float(s1[0]==s2[0])
		return (original_result+first_letter_result*first_letter_weight)/(1.0+first_letter_weight)
	return new_score_func