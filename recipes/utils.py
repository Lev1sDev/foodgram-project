from django.shortcuts import get_object_or_404

from .models import RecipeIngredient, Ingredient, Tag


def get_ingredients(post):
    ingredients = {}
    for key, name in post.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = post[f'valueIngredient_{num}']
    return ingredients


def get_tags(post):
    TAGS = {
        'breakfast': 'завтрак',
        'lunch': 'обед',
        'dinner': 'ужин'
    }
    tags = []
    for key, name in post.items():
        if key in TAGS.keys():
            tags.append(Tag.objects.get(title=TAGS[key]))
    return tags


def save_recipe(post, recipe):
    tags = get_tags(post)
    for tag in tags:
        recipe.tag.add(tag)
    objs = []
    ingredients = get_ingredients(post)
    recipe.recipeingredient.all().delete()
    for title, amount in ingredients.items():
        ingredient = get_object_or_404(Ingredient, title=title)
        objs.append(
            RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient,
                amount=int(amount)
            )
        )
    RecipeIngredient.objects.bulk_create(objs)
