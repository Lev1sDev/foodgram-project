from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('ingredients', views.search_ingredients, name='ingredients'),
    path('purchases/download', views.purchase_post, name='purchases_download'),
    path('purchases/<int:recipe_id>', views.purchase_delete, name='purchase_delete'),
    path('favorites/post', views.favorite_post, name='favorite_post'),
    path('favorites/<int:recipe_id>', views.favorite_delete, name='favorite_delete'),
    path('subscriptions/post', views.subscriptions_post, name='subscriptions_post'),
    path('subscriptions/<int:author_id>', views.subscriptions_delete, name='subscriptions_delete'),
]