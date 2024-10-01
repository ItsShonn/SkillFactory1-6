from email.policy import default

from django import template
from ..models import Category, UserToCategory

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


@register.simple_tag(takes_context=True)
def category(context, **kwargs):
	context = context['request'].GET.get('categories')
	if context:
		cat = Category.objects.get(id=context)
		return cat
	else:
		return None


@register.simple_tag(takes_context=True)
def get_sub(context, **kwargs): #Вы подписаны на {% get_sub %}
	context = context['request'].user
	subs = []
	for sub in UserToCategory.objects.filter(user=context):
		subs.append(Category.objects.get(id=sub.category.id))
	return str('Вы подписаны на ' + ', '.join([str(sub) for sub in subs])) if subs else 'Подпишитесь на что-нибудь!'