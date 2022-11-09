from django import template
from django.utils.safestring import mark_safe
import markdown

from ..forms import SearchForm

register = template.Library()


@register.filter
def model_name(obj):
	"""Defining what object is: discipline, theme or page"""
	try:
		return obj._meta.model_name
	except AttributeError:
		return None


@register.filter(name='markdown')
def markdown_format(text):
	"""Applying markdown to a page"""
	return mark_safe(markdown.markdown(text))


@register.inclusion_tag('pages/additional/navigation.html')
def navigation(curr_object):
	"""Adds a row with clickable links from main page till current page like main/discipline/theme/page"""
	nav_list = [curr_object]
	while curr_object._meta.model_name != 'discipline':
		curr_object = curr_object.content_object
		nav_list.insert(0, curr_object)
	return {'nav_list': nav_list}


@register.inclusion_tag('pages/additional/search.html')
def search_field(curr_object):
	"""Searchbar for site"""
	if curr_object._meta.model_name == 'discipline':
		discipline = curr_object.title
	else:
		discipline = curr_object.discipline_parent
	form = SearchForm(initial={'discipline': discipline})
	return {'form': form, 'discipline': discipline}


@register.inclusion_tag('pages/additional/subitem_plate.html')
def subitem_plate(item, request):
	"""Displays a plate with subitem information"""
	return {'item': item, 'request': request}


@register.inclusion_tag('pages/additional/tag_buttons.html')
def tag_buttons():
	"""Adds html-tags button panel and scripted hotkeys when creating/editing a page"""
	return None


@register.inclusion_tag('pages/additional/management_buttons.html')
def management_buttons(scenario, object=None, item_class=None):
	"""Adds different plus/edit/delete buttons for different scenarios"""
	return {'scenario': scenario, 'object': object, 'item_class': item_class}
