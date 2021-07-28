from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets

from ..users.permissions import IsAdminOrReadOnly
from .filters import TitlesFilter
from .models import Category, Genre, Title
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitleSerializerOnePost)


class CustomViewset(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        actions = ['create', 'partial_update']
        if self.action in actions:
            return TitleSerializerOnePost
        return TitleSerializer

    def get_queryset(self):
        return Title.objects.all().annotate(rating=Avg('reviews__score'))


class GenreViewSet(CustomViewset):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class CategoriesViewSet(CustomViewset):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
