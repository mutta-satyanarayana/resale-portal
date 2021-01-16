from django.shortcuts import render,redirect
#from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import UserProfile
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UpdateProfile, ViewProfile
from django.contrib.auth import logout as user_logout

# Create your views here.
'''
def register(request):
    #print("\n",request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        #print("\n\n\t",form)
        if form.is_valid():
            #print("\n\n",form)
            # form.save() #completed sign up
            # from_data = form.save(commit= False)
            messages.success(request, "Hi {} you are successfully registered".format(from_data.username))
            #return HttpResponse('Success')
            return redirect('users/login')
        else:
            messages.warning(request,form.errors)
            return redirect('/users/register')

    form = UserRegisterForm()
    context = {
               'form': form,
               }
    return render(request, 'users/register.html', context)
'''
"""
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users/login')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {
        'form': form
    })
"""

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.warning(request,"Hi {} you are successfully registered".format(form.cleaned_data['username']))
            return redirect('users:login')
        else:
            messages.warning(request,"Please Enter Correct Details...")
            redirect('users:signup')
   
    else:
        form = UserRegisterForm()
        return render(request, 'users/signup.html', {'form':form})


@login_required
def profile(request):
    user = User.objects.get(id  =request.user.id)
    pro = UserProfile.objects.get(userid = user)
    return render(request, 'users/profile.html',{'pro':pro, 'user':user})


@login_required
def editprofile(request):
    if request.method == "POST":
        update_form = UpdateProfile(request.POST,instance=request.user)
        view_form = ViewProfile(request.POST,request.FILES,instance=request.user.userprofile)
        if update_form.is_valid() and view_form.is_valid():
            update_form.save()
            view_form.save()
            messages.warning(request,"Your details are Updated successfully registered")
            return redirect("/")
        else:
            update_form = UpdateProfile(instance=request.user)
            view_form = ViewProfile(instance=request.user.userprofile)
            return HttpResponse('Not Done')
    else:
        update_form = UpdateProfile(instance=request.user)
        view_form = ViewProfile(instance=request.user.userprofile)
        return render(request,"users/editprofile.html",{'update_form':update_form,'view_form':view_form})


@login_required
def removeuser(request):

    current_user = request.user
    
    delete_user = User.objects.get(id = current_user.id)
    delete_user.delete()
    messages.warning(request, "Your Account is Removed Successfully...")
    return redirect("/")

@login_required
def logout(request):
    user_logout(request)
    return redirect('/')
