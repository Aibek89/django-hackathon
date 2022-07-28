from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer


class RegisterApiView(APIView):
    def post(self, request):
        print(dir(request))
        data = request.data
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message = f'Вы успешно зарегистрированы.' \
                      f'Вам отправлено письмо с активацией'

            return Response(message, status=201)
        print('hey')
