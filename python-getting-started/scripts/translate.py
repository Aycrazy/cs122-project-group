# CS122 Project Translate Word
#
# Ratul Esrar

import mtranslate

def translate_keywords(text_from_ui):
	'''
	Function to take keyword from Django ui and translate into spanish in order to search titles from Mexican newspaper.

	Input: text_from_ui (string)

	Output: 
	'''
	try:
		return mtranslate.translate(text_from_ui, "es", "en")

	except:
		print("Google Translate has failed us.")
