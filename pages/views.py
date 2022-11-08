from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
# from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Discipline, Theme, Page, GeneralContent
from .forms import CreatePageForm, ContentTypeForm, SearchForm


# Create your views here.
class DisciplinesView(ListView):
	queryset = Discipline.objects.all()
	template_name = 'pages/content/disciplines_list.html'

	
class DisciplineDetailView(DetailView):
	model = Discipline
	template_name = 'pages/content/discipline_detail.html'


class DisciplineCreationView(LoginRequiredMixin, CreateView):
	template_name = 'pages/management/discipline_create.html'
	model = Discipline
	fields = ('title', 'description', 'image')
	success_url = reverse_lazy('pages:disciplines_list')

		
class DisciplineEditView(LoginRequiredMixin, UpdateView):
	model = Discipline
	fields = ('title', 'description', 'image')
	template_name = 'pages/management/edit.html'

		
class DisciplineDeleteView(LoginRequiredMixin, DeleteView):
	model = Discipline
	success_url = reverse_lazy('pages:disciplines_list')
	template_name = 'pages/management/delete.html'

		
class ThemeDetailView(DetailView):
	model = Theme
	template_name = 'pages/content/theme_detail.html'

		
class ThemeEditView(LoginRequiredMixin, UpdateView):
	model = Theme
	fields = ['title', 'description']
	template_name = 'pages/management/edit.html'

		
class ThemeDeleteView(LoginRequiredMixin, DeleteView):
	model = Theme
	template_name = 'pages/management/delete.html'
	
	def get_success_url(self):
		parent = self.object.content_object
		return parent.get_absolute_url()


class PageDetailView(DetailView):
	model = Page
	template_name = 'pages/content/page_detail.html'


class PageDeleteView(LoginRequiredMixin, DeleteView):
	model = Page
	template_name = 'pages/management/delete.html'
	
	def get_success_url(self):
		parent = self.object.content_object
		return parent.get_absolute_url()

		
class PageEditView(LoginRequiredMixin, UpdateView):
	model = Page
	form_class = CreatePageForm
	template_name = 'pages/management/edit.html'


@login_required
def add_new_content(request, class_name, key):
	if class_name == 'discipline':
		current_parent = Discipline.objects.get(pk=key)
		content = list(current_parent.themes.all()) + list(current_parent.pages.all())
	else:
		current_parent = Theme.objects.get(pk=key)
		content = list(current_parent.subthemes.all()) + list(current_parent.pages.all())
	
	sidebar_title = current_parent.title
	path = current_parent.generalcontent_ptr.path
	discipline_name = path.split('/')[0]
	
	if request.method == 'POST':
		form = ContentTypeForm(discipline_name, request.POST)

		if form.is_valid():
			cd = form.cleaned_data
			if len(cd['parent'].path.split('/')) == 1:	#parent is discipline
				content_type = ContentType.objects.get(model='discipline')
				object_id = cd['parent'].discipline.pk
			else:
				content_type = ContentType.objects.get(model='theme')
				object_id = cd['parent'].theme.pk
			
			if cd['content_type'] == 'page':
				item = Page(title=cd['title'], content=cd['content'],
					content_type=content_type, object_id=object_id)
			else:
				item = Theme(title=cd['title'], description=cd['content'],
					content_type=content_type, object_id=object_id)
			
			item.save()	
			return redirect(item.get_absolute_url())

		else:
			return render(request, 'pages/management/choose_content.html',
			              {'form': form, 'parent': path, 'object_list': content, 'sidebar_title': sidebar_title,
			               'object': current_parent})

	else:
		form = ContentTypeForm(discipline=discipline_name, initial={'parent': current_parent.generalcontent_ptr, 'content_type': 'page'})
		content.sort(key=lambda x: x.title)
	return render(request, 'pages/management/choose_content.html',
			{'form': form, 'parent': path, 'object_list': content, 'sidebar_title': sidebar_title, 'object': current_parent})


class PagesLogin(LoginView):
	object_list = Discipline.objects.all()


@require_POST
def search_content(request):
	form = SearchForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		query = cd['search']
		all_themes = Theme.objects.filter(discipline_parent=cd['discipline'])
		all_pages = Page.objects.filter(discipline_parent=cd['discipline'])
		result = set(all_themes.filter(title__icontains=query)) | set(all_themes.filter(description__icontains=query)) | \
			set(all_pages.filter(title__icontains=query)) | set(all_pages.filter(content__icontains=query))

		
		discipline = Discipline.objects.get(title=cd['discipline'])
		content = list(discipline.themes.all()) + list(discipline.pages.all())
		content.sort(key=lambda x: x.title)
		
	return render(request, 'pages/content/search_result.html', {'result': result,
		'object_list': content, 'sidebar_title': discipline.title, 'object': discipline, 'search_phrase': cd['search']})
