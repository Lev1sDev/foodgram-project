from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('purchases/download/', views.purchases_download, name='download'),
    path('recipe/new/', views.new_recipe, name='new_recipe'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorites/', views.favorites, name='favorites'),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('purchases/', views.purchases, name='purchases'),
    path('<str:username>/', views.profile, name='profile'),
    path(
        '<str:username>/<int:recipe_id>/edit/', views.recipe_edit,
        name='recipe_edit'
    ),
    path('404/', views.page_not_found, name='page_not_found'),
    path('500/', views.server_error, name='server_error'),
]
