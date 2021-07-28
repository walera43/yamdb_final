from rest_framework import serializers

from .models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = (
            ['id', 'name', 'year', 'rating',
             'description', 'genre', 'category']
        )


class TitleSerializerOnePost(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ['id', 'name', 'year', 'genre', 'category', 'description']
        model = Title
