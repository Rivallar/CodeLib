from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Page, Discipline, Theme

@receiver(post_save, sender=Page)
def get_path(sender, instance, **kwargs):
	path_list = []
	obj = instance
	while True:
		path_list.insert(0, obj.title.lower())
		if obj._meta.model_name == 'discipline':
			path_list[0] = path_list[0].upper()
			break
		else:
			obj = obj.content_object
	instance.path = '|'.join(path_list)
	instance.save()
	#return '|'.join(path_list)

