from django.urls import path
from portfolio import views

urlpatterns = [
    path('', views.PortfolioTemplateView.as_view(), name='portfolio'),
    path('ticker/<str:symbol>/', views.TickerDetailView.as_view(), name='ticker_detail'),
    path('ajax/get_updated_ticker_data', views.get_updated_ticker_data, name='get_updated_ticker_data'),
]