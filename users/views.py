from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, RatingForm, ReviewForm
from .models import Watchlist, Rating
from catalog.models import Film, Review


# Create your views here.

@login_required(login_url='login')
def profile(request):
    profile = request.user.profile
    context = {'profile': profile}
    return render(request, 'users/profile.html', context)


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            print("Username doesn't exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('catalog')
        else:
            print('Login error')
    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')


def registerUser(request):
    form = CustomUserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            return redirect('catalog')

    return render(request, 'users/registration.html', context)


@login_required(login_url='login')
def editProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def watchlist(request):
    watchlist = Watchlist.objects.filter(user_id=request.user.id)
    context = {'watchlist': watchlist}
    return render(request, 'users/watchlist.html', context)


@login_required(login_url='login')
def addToWatchlist(request, film_id):
    try:
        Watchlist.objects.create(
            user=request.user,
            film=Film.objects.get(id=film_id)
        )
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        print('Already in watchlist')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def deleteFromWatchlist(request, film_id):
    try:
        Watchlist.objects.get(film_id=film_id, user_id=request.user.id).delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        print('Already deleted')
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def seenToggle(request, film_id):
    try:
        watchlistItem = Watchlist.objects.get(film_id=film_id, user_id=request.user.id)
        if watchlistItem.is_seen:
            watchlistItem.is_seen = False
        else:
            watchlistItem.is_seen = True
        watchlistItem.save()
        return redirect(request.META.get('HTTP_REFERER'))
    except:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def addRating(request, film_id):
    film = Film.objects.get(id=film_id)
    form = RatingForm(request.POST)
    if form.is_valid():
        Rating.objects.update_or_create(
            user_id=request.user.id,
            film_id=film_id,
            defaults={'star_id': int(request.POST.get('star'))}
        )
        film.calculate_rating
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='login')
def addReview(request, film_id):
    film = Film.objects.get(id=film_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.film = film
        review.user = request.user
        review.save()
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))
