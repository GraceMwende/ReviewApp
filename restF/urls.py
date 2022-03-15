from django.urls import path,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('',views.home,name='home'),
  path('search/',views.search_results, name='search_results'),
  re_path('project/(\d+)',views.project, name='project'),
  path('new/project',views.new_project, name='new-project'),
  path('user/',views.userpage,name='userpage'),
  path('addreview/<int:id>/',views.add_review,name='add_review'),
  path('api/projects/',views.ProjectList.as_view()),
  path('api/profiles/',views.ProfileList.as_view()),
  re_path('api/project/project-id/(?P<pk>[0-9]+)',views.ProjectDescription.as_view()),
  re_path('api/profile/profile-id/(?P<pk>[0-9]+)',views.ProfileDescription.as_view())
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)