# NLTK Sentiment Analysis Test
#
# Ratul Esrar

from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.sentiment import vader
import re

FILE_1 = "files-to-translate/span_eng_dict.txt"
FILE_2 = "files-to-translate/span_eng_terms.txt"
FILE_3 = "files-to-translate/wiktionary_en_sp.txt"

TRANSLATOR_DICT = get_translate_dict()

def get_translate_dict(file1=FILE_1, file2=FILE_2, file3=FILE_3):
	'''
	Takes three txt files from dict.info and returns a dictionary of spanish words with their respective english translations.

	Inputs:
		file1 (string)
		file2 (string)
		file3 (string)

	Output:
		mapped_dict (dict) 
	'''
	mapped_dict = {}
	span_words = []
	eng_words = []
	for line in open(file1):
		if ";" in line:
			l = line.split()
			s_word = l[0]
			e_word = re.sub("\n", "", l[-1])
			span_words.append(s_word.lower())
			eng_words.append(e_word.lower())
		else:
			l = line.split("\t")
			s_word = l[0]
			e_word = re.sub("\n", "", l[-1])
			span_words.append(s_word.lower())
			eng_words.append(e_word.lower())

	for line in open(file2):
		l = line.split("\t")
		s_word = l[0]
		e_word = re.sub("\n", "", l[-1])
		span_words.append(s_word.lower())
		eng_words.append(e_word.lower())

	for line in open(file3):
		if "(m)" in line or "(f)" in line:
			l = line.split()
			if len(l) < 8:
				s_word = re.sub("\n", "", l[1])
				e_word = l[0]
				span_words.append(s_word.lower())
				eng_words.append(e_word.lower())

	for x, y in zip(span_words, eng_words):
		if x in mapped_dict:
			continue
		else:
			mapped_dict[x] = y

	return mapped_dict

def translate_article(article, translator_dict=TRANSLATOR_DICT):
	'''
	Takes an article from a spanish newspaper and a python spanish-engligh dictionary, tokenizes the article using nltk, and returns a string of the translated words from the original article.

	Inputs:
		article (string)
		translator_dict (dict)

	Output:
		translation (string)
	'''
	tokens = word_tokenize(article.lower())
	lst = []
	translation = ""
	for t in tokens:
		if t in translator_dict:
			lst.append(translator_dict[t])

	for word in lst:
		translation += word + " "

	return translation

def get_nltk_score(eng_text):
	'''
	Takes an english text and returns the compound polarity score, which is a score between -1 and 1. -1 is most negative, 0 is netrual, and 1 is most positive.

	Input: eng_text (string)

	Output: compound score (float)
	'''
	s = vader.SentimentIntensityAnalyzer()
	polarity_dict = s.polarity_scores(eng_text)
	compound_score = polarity_dict["compound"]
	return compound_score






