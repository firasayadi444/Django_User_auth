from django.urls import path
from . import views

urlpatterns = [
    path('predict', views.predict_category, name='predict_category'),
    path('lastprompt', views.getlastprompt, name='last_prompt'),
]
