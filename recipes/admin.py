from django.contrib import admin

from .models import Favorite, Follow, Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    autocomplete_fields = ('ingredient',)
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('title', 'author', 'favorites_count')
    list_filter = ('title', 'author', 'tag',)
    readonly_fields = ('favorites_count',)

    def favorites_count(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('title', 'dimension',)
    list_filter = ('title',)
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(RecipeIngredient)
