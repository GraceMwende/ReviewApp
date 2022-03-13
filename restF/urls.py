from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.home,name='home'),
  path('search/',views.search_results, name='search_results'),
  re_path('project/(\d+)',views.project, name='project'),
  path('new/project',views.new_project, name='new-project')
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)