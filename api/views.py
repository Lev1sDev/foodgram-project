from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework.decorators import api_view
from .serializers import IngredientSerializer
from .models import Ingredient, Purchase, User, Recipe, Favorite, Follow


@api_view(['GET'])
def search_ingredients(request):
    text = request.GET.get('query')[0: -1]
    ingredient = Ingredient.objects.filter(title__istartswith=text)
    serializer = IngredientSerializer(ingredient, many=True)
    return JsonResponse(serializer.data, safe=False)


@login_required
@api_view(['POST'])
def purchase_post(request):
    recipe_pk = request.data['id']
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    purchase = Purchase.objects.filter(
        user=request.user, recipe__pk=recipe_pk
    ).exists()
    if not purchase:
        Purchase.objects.create(user=request.user, recipe=recipe)
    return JsonResponse({'status_code': '200'})


@login_required
@api_view(['DELETE', 'GET'])
def purchase_delete(request, recipe_id):
    purchase = Purchase.objects.filter(user=request.user, recipe__id=recipe_id)
    if purchase.exists():
        purchase.delete()
    if request.method == 'GET':
        return redirect('purchases')
    return JsonResponse({'status_code': '204'})


@login_required
@api_view(['POST'])
def favorite_post(request):
    recipe_pk = request.data['id']
    recipe = get_object_or_404(Recipe, pk=recipe_pk)
    favorite = Favorite.objects.filter(
        user=request.user, recipe__pk=recipe_pk
    ).exists()
    if not favorite:
        Favorite.objects.create(user=request.user, recipe=recipe)
    return JsonResponse({'status_code': '200'})


@login_required
@api_view(['DELETE'])
def favorite_delete(request, recipe_id):
    favorite = Favorite.objects.filter(user=request.user, recipe__id=recipe_id)
    if favorite.exists():
        favorite.delete()
    return JsonResponse({'status_code': '204'})


@login_required
@api_view(['DELETE', 'GET'])
def subscriptions_delete(request, author_id):
    following = Follow.objects.filter(user=request.user, author__id=author_id)
    if following.exists():
        following.delete()
    if request.method == 'GET':
        return redirect('follow_index')
    return JsonResponse({'status_code': '204'})


@login_required
@api_view(['POST'])
def subscriptions_post(request):
    author_id = request.data['id']
    author = get_object_or_404(User, id=author_id)
    following = Follow.objects.filter(user=request.user, author=author)
    if not following and author != request.user:
        Follow.objects.create(user=request.user, author=author)
    return JsonResponse({'status_code': '200'})
