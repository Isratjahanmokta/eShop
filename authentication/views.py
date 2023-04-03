#authentication
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

#forms and model
from .models import Profile
from authentication.forms import ProfileForm

# Create your views here.
def index(request):
    return render(request, 'base.html', context= {'title':'Home'})

def profile(request):
    profile = Profile.objects.all()
    context = {
        'profile':'profile',
        'title':'profile'
    }
    return render(request, 'authentication/profile.html', context=context)

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                form = ProfileForm(instance=profile)
    return render(request, 'authentication/user_profile.html', context={'form':form})