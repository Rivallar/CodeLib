from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from pages.models import Discipline, Theme, Page


class Command(BaseCommand):
	help = "Assigns correct parents to pages and themes after fixtures load"

	@staticmethod
	def assign(lst: list, content_discipline, disciplines_dict, content_theme, themes_dict):
		for item in lst:
			try:
				path = item.path.split('/')[:-1]
				if len(path) == 1:
					item.content_type = content_discipline
					item.object_id = disciplines_dict[path[-1].lower()]
				else:
					item.content_type = content_theme
					item.object_id = themes_dict[path[-1].lower()]
				item.save()
			except KeyError:
				print(f'Some problems with item {item}. No parent found. Probably something with paths.')
			except AttributeError:
				print(f'Still not investigated attribute_exception with item {item}')
			except:
				print(f'Unknown exception with item {item}')

	def handle(self, *args, **options):
		content_discipline = ContentType.objects.get(model='discipline')
		content_theme = ContentType.objects.get(model='theme')

		disciplines = Discipline.objects.all().values_list('title', 'id')
		disciplines_dict = {key.lower(): value for key, value in disciplines}

		themes = Theme.objects.all().select_related('generalcontent_ptr', 'generalcontent_ptr__path')
		themes_dict = {key.lower(): value for key, value in themes.values_list('title', 'id')}

		pages = Page.objects.all()

		Command.assign(themes, content_discipline, disciplines_dict, content_theme, themes_dict)
		Command.assign(pages, content_discipline, disciplines_dict, content_theme, themes_dict)
