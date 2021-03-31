from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random_page"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("<str:entry>/edit", views.edit, name="edit"),
    path("<str:entry>", views.entry, name="entry")
]

