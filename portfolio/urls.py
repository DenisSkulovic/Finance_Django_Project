from django.urls import path
from portfolio import views

urlpatterns = [
    path('', views.PortfolioTemplateView.as_view(), name='portfolio'),

]