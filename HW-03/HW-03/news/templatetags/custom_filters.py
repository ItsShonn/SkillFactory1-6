from django import template

register = template.Library()

CENSORE_WORDS = [
	'мат',
	'плохо',
	'шрек',
	'уныние'
]

@register.filter()
def censor(value):
	if type(value) is str:
		res = []
		for word in value.split(' '):
			if word.lower() in CENSORE_WORDS:
				res.append(f'{word[0]}{len(word[1:])*"*"}')
			else:
				res.append(word)
		return ' '.join(res)
	else:
		raise TypeError('Нестроковый тип данных')