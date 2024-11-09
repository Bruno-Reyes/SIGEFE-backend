from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HolaMundoView(APIView):
    def get(self, request):
        return Response({"message": "Hola mundo desde Django"}, status=status.HTTP_200_OK)
