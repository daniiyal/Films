from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('edit-profile', views.editProfile, name='edit_profile'),
    path('add-to-watchlist/<str:film_id>/', views.addToWatchlist, name='add_to_watchlist'),
    path('delete-from-watchlist/<str:film_id>/', views.deleteFromWatchlist, name='delete_from_watchlist'),
    path('seen-toggle/<str:film_id>/', views.seenToggle, name='seen_toggle'),
    path('add-rating/<str:film_id>/', views.addRating, name='add_rating'),
    path('add-review/<str:film_id>/', views.addReview, name='add_review')
]
