from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random, name="random_page"),
    path("<str:entry>", views.entry, name="entry")
]

