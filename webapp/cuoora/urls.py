from django.urls import path
from . import views

urlpatterns = [
    path("topics_list/", views.topics_list_view),
    path('social/', views.social_view, name="social"),
    path('topics_of_interest/', views.topics_of_interest_view, name="topics_of_interest"),
    path('news/', views.news_view, name="news"),
    path('popular_today/', views.popular_today_view, name="popular_today"),
    path('questions/<int:question_id>/', views.question_details_view, name='question_details'),
    path('questions/<int:question_id>/answer/', views.submit_answer, name='submit_answer'),
]