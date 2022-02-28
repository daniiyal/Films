from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Review
from users.models import Profile, RatingStar, Rating


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'email', 'username', 'password1', 'password2'
        ]
        labels = {
            'first_name': 'Имя',
            'email': 'Email адрес',
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль',

        }


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'bio', 'profile_image', 'genres', 'keyword']
        labels = {
            'name': 'Имя',
            'bio': 'О себе',
            'profile_image': 'Изображение профиля',
            'genres': 'Любимые жанры',
            'keyword': 'Ключевые слова',
        }


class RatingForm(ModelForm):
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ['star']


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Тип рецензии',
            'body': 'Текст рецензии'
        }
