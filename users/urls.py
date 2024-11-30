from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),  # Use standard naming
    path('login', LoginView.as_view(), name='login'),
    path('user/<int:user_id>', UserView.as_view(), name='user_profile'),
    path('logout', LogoutView.as_view(), name='logout'),
]
