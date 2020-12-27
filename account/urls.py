from django.urls import path
from account import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
]