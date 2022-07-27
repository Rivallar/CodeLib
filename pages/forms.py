from django import forms
from .models import Discipline, Page, Theme, GeneralContent

class CreateDisciplineForm(forms.ModelForm):
	class Meta:
		model = Discipline
		fields = ('title', 'description', 'image')
		
class CreatePageForm(forms.ModelForm):
	class Meta:
		model = Page
		fields = ('title', 'content')
		widgets = {'content': forms.Textarea(attrs={'class':'page_content'})}
		
class ContentTypeForm(forms.Form):
	parent = forms.ModelChoiceField(queryset=None)
	CHOICES = [('page', 'PAGE'), ('theme', 'THEME')]
	content_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
	title = forms.CharField()
	content = forms.CharField(widget=forms.Textarea(attrs={'class':'page_content'}))
	
	def __init__(self, discipline, *args, **kwargs):
		super().__init__(*args, **kwargs)
		discipline_name = discipline.upper()
		self.fields['parent'].queryset = GeneralContent.objects.filter(path__startswith=discipline_name). \
			values_list('path', flat=True).order_by('path')
			
class ContentTypeForm2(forms.Form):
	parent = forms.CharField()
	CHOICES = [('page', 'PAGE'), ('theme', 'THEME')]
	content_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
	title = forms.CharField()
	content = forms.CharField(widget=forms.Textarea(attrs={'class':'page_content'}))
	
class SearchForm(forms.Form):
	search = forms.CharField(max_length=50)
	discipline = forms.CharField(widget=forms.HiddenInput)	
	
	
