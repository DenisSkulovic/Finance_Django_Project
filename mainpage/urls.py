from django.urls import path
from mainpage import views


urlpatterns = [
    path('', views.MainpageTemplateView.as_view(), name = 'mainpage'),
]