from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q

from catalog.models import Film


def paginateCatalog(request, films, results):
    page = request.GET.get('page')
    results = 10
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
    return films, search_query
