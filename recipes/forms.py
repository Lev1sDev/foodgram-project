from django import forms

from .models import Recipe

errors = {
    'required': 'Поле обязательно для заполнения',
    'invalid': 'Время приготовления не может быть меньше минуты'
}


class RecipeForm(forms.ModelForm):
    time = forms.IntegerField(error_messages=errors)

    class Meta:
        model = Recipe
        fields = ('title', 'text', 'time', 'image')
