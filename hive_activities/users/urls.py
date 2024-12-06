from django.contrib.auth.views import LogoutView
from django.urls import path

from hive_activities.users import views
from hive_activities.users.views import HiveLoginView, SignUpView, ProfileDetailView, ProfileEditView, \
    ProfileDeleteView, RoleRequestView, RoleRequestManagementView, home_after_logout

app_name = 'users'

urlpatterns = [
    path('login/', HiveLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='users:home_after_logout'), name='logout'),
    path('logout/come_back/', home_after_logout, name='home_after_logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('role_change_request/', RoleRequestView.as_view(), name='role_change'),
    path('role_change_management/', RoleRequestManagementView.as_view(), name='pending_role_requests'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    path('password-reset/', views.HivePasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.HivePasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.HivePasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.HivePasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', views.HivePasswordChangeView.as_view(), name='password_change'),
]
