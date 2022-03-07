from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Film, CastAndCrew, Review, Genre, Keyword
from users.models import Watchlist, Rating
from users.forms import RatingForm, ReviewForm
from .utilities import searchFilms, paginateCatalog, filter_films


# Create your views here.

def get_watchlist(request):
    items = []
    watchlist = Watchlist.objects.filter(user_id=request.user.id)
    for item in watchlist:
        items.append(item.film.id)

    return items


def get_years():
    years = []

    for film in Film.objects.all():
        if film.release_date.year not in years:
            years.append(film.release_date.year)
    years.sort()
    return years


def get_genres():
    genres_query = Film.objects.values_list('genre__genre_name')
    genres = []
    for genre in genres_query:
        if genre[0] not in genres:
            genres.append(genre[0])
    return genres


def get_keywords():
    keywords_query = Film.objects.values_list('keyword__keyword')
    keywords = []
    for keyword in keywords_query:
        if keyword[0] not in keywords:
            keywords.append(keyword[0])
    return keywords


def catalog(request):
    films, search_query = searchFilms(request)

    watchlist = get_watchlist(request)

    genres = get_genres()
    keywords = get_keywords()
    years = get_years()

    films = filter_films(request, films, years, genres, keywords)
    print(len(films))
    custom_range, films = paginateCatalog(request, films, 12)

    context = {'films': films,
               'watchlist': watchlist,
               'search_query': search_query,
               'custom_range': custom_range,
               'years': years,
               'genres': genres,
               'keywords': keywords}
    return render(request, 'catalog/catalog.html', context)


def film_info(request, pk):
    film = Film.objects.get(id=pk)
    castandcrew = CastAndCrew.objects.filter(film__id=pk)
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    month = month_list[film.release_date.month - 1]
    rating_form = RatingForm()
    rating_user = Rating.objects.filter(film__id=pk, user_id=request.user.id)
    reviews = Review.objects.filter(film__id=pk)
    review_form = ReviewForm()

    context = {'film': film,
               'cast': castandcrew,
               'month': month,
               'month_list': month_list,
               'rating_form': rating_form,
               'rating_user': rating_user,
               'reviews': reviews,
               'review_form': review_form
               }

    return render(request, 'catalog/film.html', context)


def films_by_year(request, year):
    films = Film.objects.filter(release_date__year=year)

    custom_range, films = paginateCatalog(request, films, 14)

    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist}
    return render(request, 'catalog/catalog.html', context)


def films_by_country(request, country):
    films = Film.objects.filter(country__country=country)
    custom_range, films = paginateCatalog(request, films, 14)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist,
               'custom_range': custom_range}
    return render(request, 'catalog/catalog.html', context)


def films_by_genre(request, genre):
    films = Film.objects.filter(genre__genre_name=genre)
    custom_range, films = paginateCatalog(request, films, 14)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist,
               'custom_range': custom_range}
    return render(request, 'catalog/catalog.html', context)


def films_by_person(request, person):
    films = Film.objects.filter(castandcrew__man__id=person).distinct()
    custom_range, films = paginateCatalog(request, films, 14)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist,
               'custom_range': custom_range}
    return render(request, 'catalog/catalog.html', context)


def sort_by_date(request):
    films = Film.objects.all().order_by('-release_date')
    custom_range, films = paginateCatalog(request, films, 14)
    watchlist = get_watchlist(request)
    context = {'films': films,
               'watchlist': watchlist,
               'custom_range': custom_range}
    return render(request, 'catalog/catalog.html', context)


def sort_by_interests(request):
    user_keywords = request.user.profile.keyword.values_list('keyword')
    user_genres = request.user.profile.genres.values_list('genre_name')
    order_by_interests = []

    films = Film.objects.all()

    for film in films:
        film_keywords = film.keyword.values_list('keyword')
        film_genres = film.genre.values_list('genre_name')
        if any(x in film_keywords for x in user_keywords):
            order_by_interests.append(film)
        if any(x in film_genres for x in user_genres):
            order_by_interests.append(film)

    relevant_films = []
    for film in order_by_interests:
        if film not in relevant_films:
            relevant_films.append(film)

    watchlist = get_watchlist(request)
    custom_range, relevant_films = paginateCatalog(request, relevant_films, 14)

    context = {'films': relevant_films,
               'watchlist': watchlist,
               'custom_range': custom_range}

    return render(request, 'catalog/catalog.html', context)
