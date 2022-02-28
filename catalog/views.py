from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Film, CastAndCrew, Review
from users.models import Watchlist, Rating
from users.forms import RatingForm, ReviewForm
from .utilities import searchFilms, paginateCatalog


# Create your views here.

def get_watchlist(request):
    items = []
    watchlist = Watchlist.objects.filter(user_id=request.user.id)
    for item in watchlist:
        items.append(item.film.id)

    return items


def catalog(request):
    films, search_query = searchFilms(request)

    custom_range, films = paginateCatalog(request, films, 3)

    watchlist = get_watchlist(request)

    context = {'films': films,
               'watchlist': watchlist,
               'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'catalog/catalog.html', context)


def film_info(request, pk):
    film = Film.objects.get(id=pk)
    castandcrew = CastAndCrew.objects.filter(film__id=pk)
    month = film.release_date.strftime("%B")
    rating_form = RatingForm()
    rating_user = Rating.objects.filter(film__id=pk, user_id=request.user.id)
    reviews = Review.objects.filter(film__id=pk)
    review_form = ReviewForm()

    context = {'film': film,
               'cast': castandcrew,
               'month': month,
               'rating_form': rating_form,
               'rating_user': rating_user,
               'reviews': reviews,
               'review_form': review_form
               }

    return render(request, 'catalog/film.html', context)


def films_by_year(request, year):
    films = Film.objects.filter(release_date__year=year)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist}
    return render(request, 'catalog/catalog.html', context)


def films_by_country(request, country):
    films = Film.objects.filter(country__country=country)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist}
    return render(request, 'catalog/catalog.html', context)


def films_by_genre(request, genre):
    films = Film.objects.filter(genre__genre_name=genre)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist}
    return render(request, 'catalog/catalog.html', context)


def films_by_person(request, person):
    films = Film.objects.filter(castandcrew__man__id=person)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist}
    return render(request, 'catalog/catalog.html', context)
