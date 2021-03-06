from django.shortcuts import render,redirect
from .models import Project,Profile,Review
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import NewProjectForm,UserForm,ProfileForm,ReviewForm
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile,Project
from .serializer import ProjectSerializer,ProfileSerializer
from rest_framework import status
from .permissions import IsAdminOrReadOnly
from django.db.models import Avg

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
    
# @login_required(login_url='/accounts/login/')
def project(request,project_id):
  try:
    project = Project.objects.get(id=project_id) # select from project where id=project_id
    reviews = Review.objects.filter(project = project_id)
    # reviews_avg = (Project.objects.filter(id=project_id)
    #                                                   .annotate(avg_review=Avg('rates__rating')))

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'project.html',{'project':project,'reviews':reviews})

@login_required(login_url='/accounts/login/')
def new_project(request):
  current_user = request.user
  if request.method == 'POST':
    form = NewProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.user = current_user
      project.profile = Profile.objects.filter(user = current_user).first()
      project.save()
    
    return redirect('home')

  else:
    form = NewProjectForm()
  return render(request, 'new_project.html',{'form':form})

def userpage(request):
  Profile.objects.get_or_create(user=request.user)
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


def add_review(request,id):
  if request.user.is_authenticated:
    project = Project.objects.get(id=id)

    if request.method == "POST":
      form = ReviewForm(request.POST or None)
      if form.is_valid():
        data = form.save(commit=False)
        data.rating = request.POST['rating'] #comments same
        data.user = request.user
        data.project = project
        data.save()
        return redirect("project",id)

    else:
      form = ReviewForm()
    return render(request, 'project.html',{'form':form})

  else:
    return redirect('/accounts/login')


class ProjectList(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get(self,request,format=None):
    all_projects = Project.objects.all()
    serializers = ProjectSerializer(all_projects, many=True)
    return Response(serializers.data)

  def post(self,request,format=None):
    serializers = ProjectSerializer(data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfileList(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get(self,request,format=None):
    all_profiles = Profile.objects.all()
    serializers = ProfileSerializer(all_profiles, many=True)
    return Response(serializers.data)

  def post(self,request,format=None):
    serializers = ProfileSerializer(data=request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class ProjectDescription(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get_project(self,pk):
    try:
      return Project.objects.get(pk=pk)
    except Project.DoesNotExist:
      return Http404

  def get(self,request,pk,format=None):
    project = self.get_project(pk)
    serializers = ProjectSerializer(project)
    return Response(serializers.data)

  def put(self,request,pk,format=None):
    project = self.get_project(pk)
    serializers = ProjectSerializer(project,request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self,request,pk,format=None):
    project = self.get_project(pk)
    project.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

class ProfileDescription(APIView):
  permission_classes = (IsAdminOrReadOnly,)
  def get_profile(self,pk):
    try:
      return Profile.objects.get(pk=pk)  
    except Profile.DoesNotExist:
      return Http404

  def get(self,request,pk,format=None):
    profile = self.get_profile(pk)
    serializers = ProfileSerializer(profile)
    return Response(serializers.data)

  def put(self,request,pk,format=None):
    profile = self.get_profile(pk)
    serializers = ProfileSerializer(profile,request.data)
    if serializers.is_valid():
      serializers.save()
      return Response(serializers.data)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
