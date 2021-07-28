from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import (ConfirmationCodeSerializer, UserEmailSerializer,
                          UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_confirmation_code(request):
    serializer = UserEmailSerializer(data={
        'email': request.query_params['email']}
    )
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get('email')
        username = email.split('@')[0]
        user, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        code = default_token_generator.make_token(user)
        send_mail(
            subject='Your YaMDb confirmation code',
            message=f'"confirmation_code": "{code}"',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True
        )
        return Response(data={'email': email}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data={
        'email': request.query_params['email'],
        'confirmation_code': request.query_params['confirmation_code']}
    )
    if serializer.is_valid(raise_exception=True):
        email = serializer.validated_data.get('email')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, email=email)
        if default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)},
                            status=status.HTTP_200_OK)
        return Response({'confirmation_code': 'Неверный код подтверждения'},
                        status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
