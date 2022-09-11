# from rest_framework import viewsets
# from user import serializers
# from user import models


# class UserViewSet(viewsets.ModelViewSet):
#     serializer_class = serializers.UserSerializer
#     queryset = models.User.objects.all()

from django.contrib.auth import login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from user import serializers, tokens


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# classe para pegar os dados do usuario, requer que o usuario esteja autenticado
class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class RegisterView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        user = get_user_model()
        user.objects.create_user(**request.data)
        
        # TODO: fazer link com o email_do_usuario e o token_de_validacao
        link = get_current_site() + "????" + tokens.default_token_generator.make_token(user) + "????"
        user.email_user(
            subject="Ative sua conta do TiControla.",
            message="Acesse o seguinte link para validar a sua conta: " + link
        )
        return Response(None, status=status.HTTP_202_ACCEPTED)


# TODO: criar view para receber o link de validação do usuario e alterar o status do usuario para verificado
class VerifyAccountView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        token = request.data['token']
        
        # get user from the request email
        user = models.UserData.objects.get(email=self.request.data['email'])

        if not user:
            return

        if not tokens.default_token_generator.check_token(user, token):
            return

        user.is_verified = True
        user.save()

        return Response(None, status=status.HTTP_202_ACCEPTED)
