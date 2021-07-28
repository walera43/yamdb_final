from rest_framework import exceptions, serializers

from .models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review

    def validate(self, review):
        if self.context['view'].action != 'create':
            return review
        title_id = self.context['view'].kwargs.get('title_id')
        user = self.context['request'].user
        if Review.objects.filter(author=user, title_id=title_id).exists():
            raise exceptions.ValidationError('Такой отзыв уже существует =)')
        return review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date',)
        model = Comment
