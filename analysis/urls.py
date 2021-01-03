from django.urls import path
from analysis import views


urlpatterns = [
    path('playground/', views.PlaygroundTemplateView.as_view(), name='playground'),
    path('request/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('request/<int:pk>', views.request_detail_view, name='request_detail'),
    path('article/<int:pk>', views.article_detail_view, name='article_detail'),

    path('ajax/evaluate', views.evaluate, name='evaluate'),
    path('ajax/refresh_request_status', views.refresh_request_status, name='refresh_request_status'),
    path('ajax/load_initial_content', views.load_initial_content, name='load_initial_content'),
    path('ajax/load_article_content', views.load_article_content, name='load_article_content'),
    
]