# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from wsgiref.util import request_uri
from django.shortcuts import render
# from django.views.generic import DetailView
from django.http import HttpRequest
# from django.views.generic import ListView, UpdateView
from .forms import EditProfileFormProfileData, RegisterForm, EditProfileFormUserData
from .models import Profile
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.shortcuts import redirect
# from django.core.files.storage import FileSystemStorage as Fss


# Create your views here.
# def mainpage(request):
#     return render(request, 'account/base.html', {})

def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password1'])
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            context = {'new_user': new_user}
            return render(request, 'account/register_done.html', context)
    else:
        user_form = RegisterForm()
    return render(request, 'account/register.html', {'user_form': user_form})


# @login_required
def profile_detail(request: HttpRequest, profile_id):
    user = Profile.objects.select_related().get(user_id=profile_id)
    return render(request, 'account/profile_detail.html', {'userprof': user})


@login_required
def edit_profile_view(request: HttpRequest, profile_id):
    if request.method == "POST":
        # print(request.POST)
        form_user = EditProfileFormUserData(
            data=request.POST, 
            instance=request.user)

        form_prof = EditProfileFormProfileData(
            data=request.POST, 
            instance=request.user.profile,
            files=request.FILES
        )

        if form_user.is_valid() and form_prof.is_valid():
            user = form_user.save()
            prof = form_prof.save()
            context = {
                'u_form': user,
                'p_form': prof,
            }
            return redirect('account:profile_detail', profile_id=profile_id)
    else:
        form_user = EditProfileFormUserData(instance=request.user)
        form_prof = EditProfileFormProfileData(instance=request.user.profile)
    return render(
        request,
        'account/profile_edit.html',
        {'u_form': form_user, 'p_form': form_prof}
        )
