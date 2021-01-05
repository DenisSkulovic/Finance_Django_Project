from django.urls import path
from analysis import views


urlpatterns = [
    path('playground/', views.PlaygroundTemplateView.as_view(), name='playground'),
    path('request/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('request/delete/<int:pk>', views.RequestDeleteView.as_view(), name='request_delete'),
    path('request/<int:pk>', views.request_detail_view, name='request_detail'),
    path('article/<int:pk>', views.article_detail_view, name='article_detail'),
    path('requests/<str:mode>', views.RequestsView.as_view(), name='requests'),
    path('requests/change_privacy/', views.change_accessibility, name='change_accessibility'),


    path('ajax/refresh_processor_status', views.refresh_processor_status, name='refresh_processor_status'),

    path('ajax/playground', views.playground, name='ajax_playground'),
    path('ajax/text_example_js', views.text_example_js, name='text_example_js'),

    path('ajax/refresh_requests_status', views.refresh_requests_status, name='refresh_requests_status'),
    path('ajax/refresh_request_status', views.refresh_request_status, name='refresh_request_status'),
    path('ajax/refresh_article_status', views.refresh_article_status, name='refresh_article_status'),

    path('ajax/change_model_status_js', views.change_model_status_js, name='change_model_status_js'),

    path('ajax/requests_load_initial_content', views.requests_load_initial_content, name='requests_load_initial_content'),
    path('ajax/request_load_initial_content', views.request_load_initial_content, name='request_load_initial_content'),
    path('ajax/article_load_initial_content', views.article_load_initial_content, name='article_load_initial_content'),

    path('ajax/load_requests_request_content', views.load_requests_request_content, name='load_requests_request_content'),
    path('ajax/load_request_article_content', views.load_request_article_content, name='load_request_article_content'),
    path('ajax/load_article_text_content', views.load_article_text_content, name='load_article_text_content'),

    path('ajax/article_detail_html', views.article_detail_html, name='article_detail_html'),

]