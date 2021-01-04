from django.urls import path
from analysis import views


urlpatterns = [
    path('playground/', views.PlaygroundTemplateView.as_view(), name='playground'),
    path('request/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('request/<int:pk>', views.request_detail_view, name='request_detail'),
    path('article/<int:pk>', views.article_detail_view, name='article_detail'),

    path('ajax/playground', views.playground, name='playground'),

    path('ajax/refresh_request_status', views.refresh_request_status, name='refresh_request_status'),
    path('ajax/refresh_article_status', views.refresh_article_status, name='refresh_article_status'),

    path('ajax/change_model_status_js', views.change_model_status_js, name='change_model_status_js'),

    path('ajax/request_load_initial_content', views.request_load_initial_content, name='request_load_initial_content'),
    path('ajax/article_load_initial_content', views.article_load_initial_content, name='article_load_initial_content'),

    path('ajax/load_request_article_content', views.load_request_article_content, name='load_request_article_content'),
    path('ajax/load_article_text_content', views.load_article_text_content, name='load_article_text_content'),
    path('ajax/article_detail_html', views.article_detail_html, name='article_detail_html'),
]