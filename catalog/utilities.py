from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q

from catalog.models import Film


def paginateCatalog(request, films, results):
    page = request.GET.get('page')
    paginator = Paginator(films, results)

    try:
        films = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        films = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        films = paginator.page(page)

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)
    return custom_range, films


def searchFilms(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    films = Film.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(castandcrew__man__name__icontains=search_query) |
        Q(genre__genre_name__icontains=search_query) |
        Q(release_date__year__iexact=search_query)
    )

    print(search_query)
    print(len(films))
    return films, search_query


def filter_films(request, films, years, genres, keywords):
    filter_query = {
        'year': years,
        'genre': genres,
        'keyword': keywords
    }

    if request.GET.getlist('year'):
        filter_query['year'] = request.GET.getlist('year')
        print(filter_query['year'])
    if request.GET.getlist('genre'):
        filter_query['genre'] = request.GET.getlist('genre')
        print(filter_query['genre'])
    if request.GET.getlist('keyword'):
        filter_query['keyword'] = request.GET.getlist('keyword')



    filtered_films = films.distinct().filter(
        Q(release_date__year__in=filter_query['year']) &
        Q(genre__genre_name__in=filter_query['genre']) &
        Q(keyword__keyword__in=filter_query['keyword'])
    )

    return filtered_films
