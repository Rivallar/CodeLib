from django.utils.datastructures import MultiValueDictKeyError

from .models import Discipline, Theme, Page


def uri_path(request):

	"""Returns context data to fill in sidebar panel. Context is determined from request URI"""

	def get_sidebar_content(identity, is_discipline=True):

		"""Takes required content from database"""

		if is_discipline:
			if identity.isdigit():
				content_object = Discipline.objects.get(id=int(identity))
			else:
				content_object = Discipline.objects.get(slug=identity)
			sidebar_objects = list(content_object.themes.all()) + list(content_object.pages.all())
		else:
			content_object = Theme.objects.get(id=int(identity))
			sidebar_objects = list(content_object.subthemes.all()) + list(content_object.pages.all())

		sidebar_objects.sort(key=lambda x: x.title)
		sidebar_header = content_object.title

		return sidebar_objects, sidebar_header

	path = request.path.strip('/').split('/')

	# if URI is localhost/login/ use URI from 'next' parameter or main page if not exist
	if 'login' in path:
		try:
			path = request.GET['next'].strip('/').split('/')
		except MultiValueDictKeyError:
			pass

	#sidebar for /search/ remains same as it was before search
	if 'search' in path:
		path = request.META['HTTP_REFERER'].strip('/').split('/')[-2:]

	path_set = set(path)

	# no context for admin
	if 'admin' in path:
		sidebar_objects = None
		sidebar_header = None
	# list of disciplines
	elif {'', 'create_discipline', 'login'} & path_set:
		sidebar_objects = Discipline.objects.all().order_by('title')
		sidebar_header = 'DISCIPLINES'
	# single discipline contents
	elif {'discipline', 'edit_discipline', 'delete_discipline'} & path_set:
		sidebar_objects, sidebar_header = get_sidebar_content(path[-1])
	# single theme contents
	elif {'theme', 'delete_theme', 'edit_theme'} & path_set:
		sidebar_objects, sidebar_header = get_sidebar_content(path[-1], False)
	# contents of a parent of a page
	elif {'page', 'edit_page', 'delete_page'} & path_set:
		parent = Page.objects.get(id=int(path[-1])).content_object
		parent_is_discipline = False
		if parent._meta.model_name == 'discipline':
			parent_is_discipline = True
		sidebar_objects, sidebar_header = get_sidebar_content(str(parent.id), parent_is_discipline)
	else:
		sidebar_objects = None
		sidebar_header = None

	return {'path': path, 'sidebar_objects': sidebar_objects, 'sidebar_header': sidebar_header}
