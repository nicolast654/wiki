from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("random", views.random_pick, name="random"),
    path("edit/<str:entryName>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.entry, name="entry")
]
