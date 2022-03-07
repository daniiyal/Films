from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('film/<str:pk>/', views.film_info, name='film_info'),
    path('year/<str:year>', views.films_by_year, name='films_by_year'),
    path('country/<str:country>', views.films_by_country, name='films_by_country'),
    path('genre/<str:genre>', views.films_by_genre, name='films_by_genre'),
    path('person/<str:person>', views.films_by_person, name='films_by_person'),
    path('sort-by-date', views.sort_by_date, name='sort_by_date'),
    path('sort-by-interests', views.sort_by_interests, name='sort_by_interests'),
]
