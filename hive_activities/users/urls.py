from django.contrib.auth.views import LogoutView
from django.urls import path

from hive_activities.users.views import HiveLoginView,SignUpView, ProfileDetailView, ProfileEditView, ProfileDeleteView

app_name = 'users'

urlpatterns = [
    path('login/', HiveLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]
