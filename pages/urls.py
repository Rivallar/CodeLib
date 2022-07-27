from . import views
from django.urls import path

app_name = 'pages'

urlpatterns = [
	path('management/create_discipline/', views.DisciplineCreationView.as_view(), name='discipline_create'),
	path('management/delete_discipline/<pk>/', views.DisciplineDeleteView.as_view(), name='discipline_delete'),
	path('management/edit_discipline/<slug:slug>/', views.DisciplineEditView.as_view(), name='discipline_edit'),
	path('management/delete_theme/<pk>/', views.ThemeDeleteView.as_view(), name='theme_delete'),
	path('management/edit_theme/<pk>/', views.ThemeEditView.as_view(), name='theme_edit'),
	path('management/delete_page/<pk>/', views.PageDeleteView.as_view(), name='page_delete'),
	path('management/edit_page/<pk>/', views.PageEditView.as_view(), name='page_edit'),
	path('discipline/<slug:slug>/', views.DisciplineDetailView.as_view(), name='discipline_view'),
	path('theme/<pk>/', views.ThemeDetailView.as_view(), name='theme_view'),
	path('page/<pk>/', views.PageDetailView.as_view(), name='page_view'),
	path('add_content/<str:class_name>/<int:key>', views.add_new_content, name='new_content'),
	path('search/', views.search_content, name='search'),
	path('', views.DisciplinesView.as_view(), name='disciplines_list'),
]
