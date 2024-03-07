from django.urls import path

# from news_app.views import list_view, detail_view
# from .views import ListView, DetailView
from .views import (HomePageView, NewsCategoryListGenericView, ContactGenericView,
                    create_delete_like_news, NewsDetailView)

urlpatterns = [
    # urls for function views
    # path('list/', list_view, name='news-list'),
    # path('<int:pk>/', detail_view, name='news-detail'),

    # urls for basic class views
    # path('list/', ListView.as_view(), name='news-list'),
    # path('<int:pk>/', DetailView.as_view(), name='news-detail'),

    # urls for generics
    path('', HomePageView.as_view(), name='home'),
    path('category/<slug:slug>/news/', NewsCategoryListGenericView.as_view(), name='category-news'),
    # path('news/<slug:slug>/', DetailGenericView.as_view(), name='news-detail'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/<slug:slug>/like/', create_delete_like_news, name='like'),
    path('contact/', ContactGenericView.as_view(), name='contact'),
]
