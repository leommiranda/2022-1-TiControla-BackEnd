from user_data import serializers
from user_data import models
from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from django.contrib.auth import get_user


# classe para mostrar/atualizar os dados do usuario, requer que o usuario esteja autenticado
class UserDataView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserDataSerializer

    def get_object(self):
        # returns the data that belongs to the user
        return models.UserData.objects.get(email=self.request.user.email)

    def patch_object(self):
        # updates the user's data
        models.UserData.objects.get(email=self.request.user.email).patch(**self.request.data)
        return Response(None, status=status.HTTP_202_ACCEPTED)
