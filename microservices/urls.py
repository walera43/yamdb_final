from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .reviews.views import CommentViewSet, ReviewViewSet
from .titles.views import CategoriesViewSet, GenreViewSet, TitleViewSet
from .users.views import UserViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='title')
router.register('genres', GenreViewSet, basename='genre')
router.register('categories', CategoriesViewSet, basename='category')
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='Review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='Comment'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('microservices.users.urls')),
]
