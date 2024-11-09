from django.urls import path
from views.views import HolaMundoView

urlpatterns = [
    path('hola-mundo/', HolaMundoView, name="hola-mundo"),
]
