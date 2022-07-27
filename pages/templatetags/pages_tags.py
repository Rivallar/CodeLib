from django import template
from django.utils.safestring import mark_safe
import markdown

from ..models import Page, Theme, Discipline
from ..forms import SearchForm

register = template.Library()

@register.filter
def model_name(obj):
	try:
		return obj._meta.model_name
	except AttributeError:
		return None
		
@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))
	
@register.inclusion_tag('pages/additional/navigation.html')
def navigation(curr_object):
	nav_list = [curr_object]
	while curr_object._meta.model_name != 'discipline':
		curr_object = curr_object.content_object
		nav_list.insert(0, curr_object)
	return {'nav_list': nav_list}

@register.inclusion_tag('pages/additional/search.html')
def search_field(curr_object):
	if curr_object._meta.model_name == 'discipline':
		discipline = curr_object.title
	else:
		discipline = curr_object.discipline_parent
	form = SearchForm(initial={'discipline': discipline})
	return {'form': form, 'discipline': discipline }
