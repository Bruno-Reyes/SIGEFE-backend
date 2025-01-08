from django.urls import path
from ALC000_sistema_base.views.views import ObtainCustomTokenView, LiderLecListView


urlpatterns = [
    path('token/', ObtainCustomTokenView.as_view(), name='token_obtain_pair'),
    path('lideres-lec/', LiderLecListView.as_view(), name='lideres_lec_list'),
]
