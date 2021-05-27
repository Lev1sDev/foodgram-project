from django.contrib import admin

from .models import Recipe, Ingredient, Tag, RecipeIngredient, Follow, Favorite


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('title', 'author',)
    list_filter = ('title', 'author', 'tag',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('title', 'dimension',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(RecipeIngredient)
admin.site.register(Follow)
admin.site.register(Favorite)

