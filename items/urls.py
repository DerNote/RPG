from django.urls import path, include
from . import views

urlpatterns = [
    path('RPG/' , views.index, name='Character'),
    path('RPG/compendium', views.compendium, name='Compendium'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.rederect),
    path('RPG/random', views.randominium),
    path('RPG/view/<str:name>',views.Player, name='view'),
    path('RPG/edit/<str:name>', views.Edit_character, name='Edit-character'),
    path('RPG/save/<str:name>', views.update, name='update'),
    path('RPG/iframe', views.iframe_test),
]