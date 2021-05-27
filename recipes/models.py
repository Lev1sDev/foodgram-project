from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(
        max_length=30, unique=True, verbose_name='Название'
    )
    dimension = models.CharField(
        max_length=30, verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор'
    )
    title = models.CharField(max_length=60, verbose_name='Название')
    image = models.ImageField(verbose_name='Картинка')
    text = models.TextField(verbose_name='Описание')
    ingredient = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиент',
        through='RecipeIngredient', related_name='recipes'
    )
    tag = models.ManyToManyField(
        Tag, verbose_name='Тэг', related_name='recipes'
    )
    time = models.PositiveIntegerField(verbose_name='Время приготовления')
    slug = models.SlugField(verbose_name='Slug', unique=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipeingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент', on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    amount = models.PositiveIntegerField(verbose_name='Количество')


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_follow'
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="favorites"
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="favorites"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorite'
            )
        ]


