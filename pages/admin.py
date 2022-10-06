from django.contrib import admin
from .models import Discipline, Theme, Page, GeneralContent

# Register your models here.
@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
	list_display = ('pk', 'title', 'slug', 'description', 'path')
	search_fields = ('title', 'description')
	prepopulated_fields = {'slug': ('title',)}
	#date_hierarchy = 'created'
	ordering = ('title',)
	
@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
	list_display = ('pk', 'title', 'discipline_parent', 'description', 'content_object', 'path')
	search_fields = ('title', 'description')
	prepopulated_fields = {'slug': ('title',)}
	#date_hierarchy = 'created'
	ordering = ('title',)
	
@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
	list_display = ('pk', 'title', 'discipline_parent', 'content_object', 'path')
	search_fields = ('title', 'content')
	prepopulated_fields = {'slug': ('title',)}
	date_hierarchy = 'created'
	ordering = ('title',)

@admin.register(GeneralContent)
class GeneralContentAdmin(admin.ModelAdmin):
	list_display = ('path', )




