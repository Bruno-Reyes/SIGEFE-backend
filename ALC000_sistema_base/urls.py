from django.urls import path
from ALC000_sistema_base.views.views import ObtainCustomTokenView

urlpatterns = [
    path('token/', ObtainCustomTokenView.as_view(), name='token_obtain_pair'),
]
