from django.shortcuts import render
from basicApp.forms import UserForm, UserProfileInfoForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from basicApp.models import UserProfileInfo
from ProFive.settings import MEDIA_URL, MEDIA_ROOT
# Create your views here.
def index(request):
    return render(request,'basicApp/index.html')


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basicApp:index'))


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            try:
                validate_password(password=password,user=user)
                user.set_password(user.password)
                user.save()
            except ValidationError as e :
                user_form.add_error('password',ValidationError)
                return HttpResponse('Password does not meet criteria')
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basicApp/registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('basicApp:index'))
            else:
                return HttpResponse("Account Not Active")
        else:
            print('Someone tried to log in and failed')
            print(f'Username {username} and password {password}')
            return HttpResponse('Invalid Login Details Supplied')
    else:
        return render(request,'basicApp/login.html')

@login_required
def special(request):
    user = request.user
    username = user.username
    print(username)
    user_info = UserProfileInfo.objects.get(user__username=username)
    print(user_info)
    profile_picture = user_info.profile_pic
    print(profile_picture)
    return render(request,'basicApp/special.html',{'username':username,'profile_picture':profile_picture,
                                                    'MEDIA_URL':MEDIA_URL})
