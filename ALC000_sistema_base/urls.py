from django.urls import path
from ALC000_sistema_base.views.views import ObtainCustomTokenView, LiderLecListView, LecListView


urlpatterns = [
    path('token/', ObtainCustomTokenView.as_view(), name='token_obtain_pair'),
    path('lideres-lec/', LiderLecListView.as_view(), name='lideres_lec_list'),
    path('lec/', LecListView.as_view(), name='lec_list'),
]
