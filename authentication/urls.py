from django.urls import path
from authentication.views import profile, user_profile

app_name = 'authentication'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('edit-profile/', user_profile, name='edit_profile'),
]
