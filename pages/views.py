from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Discipline, Theme, Page, GeneralContent
from .forms import CreateDisciplineForm, CreatePageForm, ContentTypeForm, ContentTypeForm2, SearchForm

# Create your views here.
class DisciplinesView(ListView):
	queryset = Discipline.objects.all()
	template_name = 'pages/content/disciplines_list.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['section'] = 'main'
		return context
	
class DisciplineDetailView(DetailView):
	model = Discipline
	template_name = 'pages/content/discipline_detail.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		content = list(self.object.themes.all()) + list(self.object.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = self.object.title
		return context

class DisciplineCreationView(LoginRequiredMixin, CreateView):
	template_name = 'pages/management/discipline_create.html'
	form_class = CreateDisciplineForm
	success_url = reverse_lazy('pages:disciplines_list')
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['object_list'] = Discipline.objects.all()
		context['section'] = 'main'
		return context
		
class DisciplineEditView(LoginRequiredMixin, UpdateView):
	model = Discipline
	fields = ['title', 'description', 'image']
	template_name = 'pages/management/edit.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		content = list(self.object.themes.all()) + list(self.object.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = self.object.title
		return context
		
class DisciplineDeleteView(LoginRequiredMixin, DeleteView):
	model = Discipline
	success_url = reverse_lazy('pages:disciplines_list')
	template_name = 'pages/management/delete.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		content = list(self.object.themes.all()) + list(self.object.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = self.object.title
		return context
		
class ThemeDetailView(DetailView):
	model = Theme
	template_name = 'pages/content/theme_detail.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		content = list(self.object.subthemes.all()) + list(self.object.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = self.object.title
		return context
		
class ThemeEditView(LoginRequiredMixin, UpdateView):
	model = Theme
	fields = ['title', 'description']
	template_name = 'pages/management/edit.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		content = list(self.object.subthemes.all()) + list(self.object.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = self.object.title
		return context
		
class ThemeDeleteView(LoginRequiredMixin, DeleteView):
	model = Theme
	template_name = 'pages/management/delete.html'
	
	def get_success_url(self):
		parent = self.object.content_object
		return parent.get_absolute_url()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		content = list(self.object.subthemes.all()) + list(self.object.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = self.object.title
		return context

class PageDetailView(DetailView):
	model = Page
	template_name = 'pages/content/page_detail.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		parent = self.object.content_object
		if parent._meta.model_name == 'discipline':
			content = list(parent.themes.all()) + list(parent.pages.all())
		else:
			content = list(parent.subthemes.all()) + list(parent.pages.all())
		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = parent.title
		return context

class PageDeleteView(LoginRequiredMixin, DeleteView):
	model = Page
	template_name = 'pages/management/delete.html'
	
	def get_success_url(self):
		parent = self.object.content_object
		return parent.get_absolute_url()
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		parent = self.object.content_object
		if parent._meta.model_name == 'discipline':
			content = list(parent.themes.all()) + list(parent.pages.all())

		else:
			content = list(parent.subthemes.all()) + list(parent.pages.all())

		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = parent.title
		return context
		
class PageEditView(LoginRequiredMixin, UpdateView):
	model = Page
	form_class = CreatePageForm
	template_name = 'pages/management/edit.html'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		parent = self.object.content_object
		if parent._meta.model_name == 'discipline':
			content = list(parent.themes.all()) + list(parent.pages.all())

		else:
			content = list(parent.subthemes.all()) + list(parent.pages.all())

		content.sort(key=lambda x: x.title)
		context['object_list'] = content
		context['sidebar_title'] = parent.title
		return context

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
		form = ContentTypeForm2(request.POST)
		if form.is_valid():

			cd = form.cleaned_data

			if len(cd['parent'].split('/')) == 1:	#parent is discipline
				content_type = ContentType.objects.get(model='discipline')
				object_id = GeneralContent.objects.get(path=cd['parent']).discipline.pk
			else:
				content_type = ContentType.objects.get(model='theme')
				object_id = GeneralContent.objects.get(path=cd['parent']).theme.pk
			
			if cd['content_type'] == 'page':
				item = Page(title=cd['title'], content=cd['content'],
					content_type=content_type, object_id=object_id)
				
			else:
				item = Theme(title=cd['title'], description=cd['content'],
					content_type=content_type, object_id=object_id)
			
			item.save()	
			return redirect(item.get_absolute_url())

		return HttpResponse('Form is bad')
		
	else:
		form = ContentTypeForm(discipline=discipline_name, initial={'parent': path, 'content_type': 'page'})
		content.sort(key=lambda x: x.title)
	return render(request, 'pages/management/choose_content.html',
			{'form': form, 'parent': path, 'object_list': content, 'sidebar_title': sidebar_title, 'object': current_parent})

class PagesLogin(LoginView):
	object_list = Discipline.objects.all()
	extra_context = {'object_list': object_list, 'section': 'main'}

@require_POST
def search_content(request):
	form = SearchForm(request.POST)
	if form.is_valid():
		cd = form.cleaned_data
		query = SearchQuery(f"{cd['search']}:*", search_type="raw")
		
		page_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
		page_headline = SearchHeadline('content', query, start_sel='<span class="highlight">', stop_sel='</span>')
		
		theme_vector = SearchVector('title', weight='A') + SearchVector('description', weight='C')
		#theme_headline = SearchHeadline('description', query, start_sel='<span class="highlight">', stop_sel='</span>')
		
		result = list(Theme.objects.filter(discipline_parent=cd['discipline']). \
			annotate(rank=SearchRank(theme_vector, query)). \
			filter(rank__gte=0.001).order_by('-rank'))
		result += list(Page.objects.filter(discipline_parent=cd['discipline']). \
			annotate(rank=SearchRank(page_vector, query)).annotate(headline=page_headline). \
			filter(rank__gte=0.001).order_by('-rank'))
		result.sort(key=lambda x: x.rank, reverse=True)
		
		
		discipline = Discipline.objects.get(title=cd['discipline'])
		content = list(discipline.themes.all()) + list(discipline.pages.all())
		content.sort(key=lambda x: x.title)
		
	return render(request, 'pages/content/search_result.html', {'result': result,
		'object_list': content, 'sidebar_title': discipline.title, 'object': discipline, 'search_phrase': cd['search']})
		
