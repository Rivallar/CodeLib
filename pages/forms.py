from django import forms

from .models import Page, GeneralContent
from .validators import exclude_slash


class CreatePageForm(forms.ModelForm):
	class Meta:
		model = Page
		fields = ('title', 'content')
		widgets = {'content': forms.Textarea(attrs={'class': 'page_content'})}


class ContentTypeForm(forms.Form):
	parent = forms.ModelChoiceField(queryset=GeneralContent.objects.all().order_by('path'))
	CHOICES = [('page', 'PAGE'), ('theme', 'THEME')]
	content_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
	title = forms.CharField(validators=[exclude_slash])
	content = forms.CharField(widget=forms.Textarea(attrs={'class': 'page_content'}))

	def __init__(self, discipline=None, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if discipline:
			discipline_name = discipline.upper()
			self.fields['parent'].queryset = GeneralContent.objects.filter(path__startswith=discipline_name).order_by('path')


class SearchForm(forms.Form):
	search = forms.CharField(max_length=50)
	discipline = forms.CharField(widget=forms.HiddenInput)
	obj_path = forms.CharField(widget=forms.HiddenInput)
	
	
