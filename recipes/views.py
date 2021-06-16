import io

import pdfkit
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template

from foodgram.settings import PAGE_SIZE

from .forms import RecipeForm
from .models import (Favorite, Follow, Purchase, Recipe, RecipeIngredient, Tag,
                     User)
from .utils import get_ingredients, get_tags, save_recipe


def index(request):
    tags = Tag.objects.all()
    recipes = Recipe.objects.all()
    objs = []
    if request.GET.get('tag'):
        for tag in request.GET.getlist('tag'):
            objs.append(Tag.objects.get(slug=tag))
        recipes = Recipe.objects.filter(tag__in=objs)
    paginator = Paginator(recipes, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'index.html', {
            'page': page, 'paginator': paginator, 'tags': tags, 'objs': objs
        }
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    following = Follow.objects.filter(
        author=recipe.author.id, user=request.user.id
    )
    return render(request, 'recipe.html', {
        'recipe': recipe,
        'following': following,
    })


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = author.recipes.all()
    tags = Tag.objects.all()
    objs = []
    if request.GET.get('tag'):
        for tag in request.GET.getlist('tag'):
            objs.append(Tag.objects.get(slug=tag))
        recipes = author.recipes.filter(tag__in=objs)
    paginator = Paginator(recipes, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    following = Follow.objects.filter(
        author=author.id, user=request.user.id
    )
    return render(request, 'profile.html', {
        'author': author,
        'page': page,
        'paginator': paginator,
        'following': following,
        'tags': tags,
        'objs': objs,
    })


@login_required
def follow_index(request):
    authors = User.objects.filter(following__user=request.user)
    paginator = Paginator(authors, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'follow.html', {'page': page, 'paginator': paginator}
    )


@login_required()
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    tags = get_tags(request.POST)
    ingredients = get_ingredients(request.POST)
    if not form.is_valid() or not tags or not ingredients:
        return render(
            request, 'new_recipe.html', {'form': form}
        )
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        save_recipe(request.POST, recipe)
    return redirect('index')


@login_required
def recipe_edit(request, username, recipe_id):
    if not request.user.username == username:
        return redirect('recipe', username, recipe_id)
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    count = recipe.recipeingredient.count()
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    if 'btn2' in request.POST:
        recipe.delete()
        return redirect('index')
    tags = get_tags(request.POST)
    ingredients = get_ingredients(request.POST)
    if not form.is_valid() or not tags or not ingredients:
        return render(
            request, 'new_recipe.html', {
                'form': form, 'recipe': recipe, 'count': -count
            }
        )
    with transaction.atomic():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        save_recipe(request.POST, recipe)
    return redirect('recipe', username, recipe_id)


@login_required
def purchases(request):
    purchases = Purchase.objects.filter(user=request.user)
    return render(request, 'purchase.html', {'purchases': purchases})


@login_required
def favorites(request):
    tags = Tag.objects.all()
    favorites = Favorite.objects.filter(user=request.user)
    objs = []
    if request.GET.get('tag'):
        for tag in request.GET.getlist('tag'):
            objs.append(Tag.objects.get(slug=tag))
        favorites = Favorite.objects.filter(
            recipe__tag__in=objs, user=request.user
        )
    paginator = Paginator(favorites, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorite.html', {
        'page': page, 'paginator': paginator, 'tags': tags, 'objs': objs
    })


def create_pdf(template_name, context):
    pdf_options = {'page-size': 'A4', 'encoding': 'UTF-8', }
    html = get_template(template_name).render(context)
    return pdfkit.from_string(html, False, options=pdf_options)


@login_required
def purchases_download(request):
    ingredients = RecipeIngredient.objects.values(
        'ingredient__title', 'ingredient__dimension').filter(
        recipe__purchases__user=request.user).annotate(amount=Sum('amount'))
    pdf = create_pdf('misc/shop_list.html', {'ingredients': ingredients}
                     )
    return FileResponse(
        io.BytesIO(pdf), filename='shop_list.pdf', as_attachment=True
    )


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
