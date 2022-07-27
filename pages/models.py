from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class GeneralContent(models.Model):
	path = models.CharField(blank=True, max_length=250)
	#created = models.DateField(auto_now_add=True, db_index=True)


class Page(models.Model):
	discipline_parent = models.CharField(max_length=250, blank=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, unique_for_date='created', blank=True)
	content = models.TextField(blank=True)
	created = models.DateField(auto_now_add=True)
	path = models.CharField(blank=True, max_length=250)
	
	content_type = models.ForeignKey(ContentType, null=True,
		on_delete=models.CASCADE, limit_choices_to={'model__in': ('discipline', 'theme')})
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	
	def __str__(self):
		return self.title
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		path_list = []
		x = self
		while True:
			path_list.insert(0, x.title.lower())
			if x._meta.model_name == 'discipline':
				self.discipline_parent = x.title
				path_list[0] = path_list[0].upper()
				break
			else:
				x = x.content_object
		self.path = '/'.join(path_list)
		super().save(*args, **kwargs)
		 
		
		
	def get_absolute_url(self):
		return reverse('pages:page_view',
			args=[self.pk])
		
		
	class Meta:
		ordering = ('title',)
		
class Theme(GeneralContent):
	generalcontent_ptr = models.OneToOneField(GeneralContent, on_delete=models.CASCADE,
		parent_link=True, primary_key=True, related_name='theme')
	discipline_parent = models.CharField(max_length=250, blank=True)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, blank=True)
	description = models.TextField(blank=True)
	pages = GenericRelation(Page)
	subthemes = GenericRelation('self')
	
	
	content_type = models.ForeignKey(ContentType, null=True,
		on_delete=models.CASCADE, limit_choices_to={'model__in': ('discipline', 'theme')})
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	
	
	def __str__(self):
		return self.title
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		path_list = []
		x = self
		while True:
			path_list.insert(0, x.title.lower())
			if x._meta.model_name == 'discipline':
				self.discipline_parent = x.title
				path_list[0] = path_list[0].upper()
				break
			else:
				x = x.content_object
		self.path = '/'.join(path_list)
		super().save(*args, **kwargs)
		
	def get_absolute_url(self):
		return reverse('pages:theme_view',
			args=[self.pk])
		
	class Meta:
		ordering = ('title',)

class Discipline(GeneralContent):
	generalcontent_ptr = models.OneToOneField(GeneralContent, on_delete=models.CASCADE,
		parent_link=True, primary_key=True, related_name='discipline')
	title = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=250, blank=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='pages/%Y/%m/%d', blank=True)
	pages = GenericRelation(Page)
	themes = GenericRelation(Theme)
	
	def __str__(self):
		return self.title
		
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		path_list = []
		x = self
		while True:
			path_list.insert(0, x.title.lower())
			if x._meta.model_name == 'discipline':
				path_list[0] = path_list[0].upper()
				break
			else:
				x = x.content_object
		self.path = '|'.join(path_list)
		super().save(*args, **kwargs)
		
	def get_absolute_url(self):
		return reverse('pages:discipline_view',
			args=[self.slug])
		
	class Meta:
		ordering = ('title',)




