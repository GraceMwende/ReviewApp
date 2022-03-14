from django.shortcuts import render,redirect
from .models import Project,Profile
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .forms import NewProjectForm,UserForm,ProfileForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile,Project
from .serializer import ProjectSerializer,ProfileSerializer

# Create your views here.
def home(request):
  projects = Project.display_projects()
  return render(request,'home.html',{'projects':projects})

def search_results(request):
  if 'project' in request.GET and request.GET['project']:
    search_term = request.GET.get('project')
    searched_projects = Project.search_by_title(search_term)
    message = f'{search_term}'  

    return render(request,'search.html',{'messages':message,'projects':searched_projects})

  else:
    message="You haven't searched for any item"
    return render(request,'search.html',{'messages':message})
    
@login_required(login_url='/accounts/login/')
def project(request,project_id):
  try:
    project = Project.objects.get(id=project_id)
  except ObjectDoesNotExist:
    raise Http404()
  return render(request,'project.html',{'project':project})
  redirect('/')

@login_required(login_url='/accounts/login/')
def new_project(request):
  current_user = request.user
  if request.method == 'POST':
    form = NewProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.user = current_user
      project.save()
    
    return redirect('home')

  else:
    form = NewProjectForm()
  return render(request, 'new_project.html',{'form':form})

def userpage(request):
  if request.method == "POST":
    user_form = UserForm(request.POST,instance=request.user)
    profile_form = ProfileForm(request.POST, request.FILES,instance=request.user.profile)

    if user_form.is_valid():
      user_form.save() 
      messages.success(request,('Your profile was successfully updated'))

    elif profile_form.is_valid():
      profile_form.save()
      messages.success(request,('Your credentials were successfully updated!'))

    else:
      messages.error(request,('Unable to complete the request'))

    return redirect('userpage')
    
  user_form = UserForm(instance=request.user)
  profile_form = ProfileForm(instance=request.user.profile)

  user = request.user
  my_projects = Project.objects.filter(user=user)

  return render(request=request, template_name='profile/user.html',context={'user':request.user,'user_form':user_form,'profile_form':profile_form,'my_projects':my_projects})

class ProjectList(APIView):
  def get(self,request,format=None):
    all_projects = Project.objects.all()
    serializers = ProjectSerializer(all_projects, many=True)
    return Response(serializers.data)

class ProfileList(APIView):
  def get(self,request,format=None):
    all_profiles = Profile.objects.all()
    serializers = ProfileSerializer(all_profiles, many=True)
    return Response(serializers.data)

  