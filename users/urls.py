from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, UserListView, UserDetailView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('users', UserListView.as_view()),  # For listing all users
    path('users/<int:pk>', UserDetailView.as_view()),  # For individual user CRUD operations
]
