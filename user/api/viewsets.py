from rest_framework import viewsets
from .serializers import UserSerializers
from django.contrib.auth.models import User


class UserViewsets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers