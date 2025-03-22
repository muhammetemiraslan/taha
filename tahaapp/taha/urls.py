from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("account/", include("account.urls")),
    # path('news/details/', views.news_details, name='news_details'),
    path('news/details/<int:id>/', views.news_details, name='news_details'),
]
