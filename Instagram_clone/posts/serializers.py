from django.contrib.auth.models import User

from rest_framework import serializers

from posts.models import Posts, Comment


class PostListSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    creator = serializers.ReadOnlyField(source='creator.username')
    image = serializers.ImageField(required=True)
    created_time = serializers.DateField(read_only=True)

    class Meta:
        model = Posts
        fields = ['id', 'creator', 'caption', 'image', 'created_time']

    def create(self, validated_data):
        return Posts.objects.create(creator=self.context['creator'], **validated_data)


class PostDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Posts
        exclude = ['id']
        extra_kwargs = {
            "image": {"read_only": True},
            "creator": {"read_only": True}
        }

    def update(self, instance, validated_data):
        instance.caption = validated_data.get('caption', instance.caption)
        instance.save()
        return instance


class AuthorSerializer(serializers.ModelSerializer):
    """
    serializer to get user
    """
    class Meta:
        model = User
        fields = ('username',)


class CommentSerializer(serializers.ModelSerializer):
    """
    serializer to get comments
    """
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created_time')
        read_only_fields = ('author', 'id', 'created_time')


class NestedComment(serializers.ModelSerializer):
    """
    serializer to get comments for ShowLikesCommentsSerializer
    """
    author = serializers.CharField(source='author.username')

    class Meta:
        model = Comment
        exclude = ['id', 'post']


class ShowLikesCommentsSerializer(serializers.ModelSerializer):
    """
    serializer to get all likes and comments for all posts per user
    """
    posts_comments = NestedComment(read_only=True, many=True)
    creator = serializers.CharField(source='creator.username')
    likes = AuthorSerializer(read_only=True, many=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Posts
        fields = ['id', 'creator', 'created_time', 'image', 'caption',
                  'posts_comments', 'likes', 'likes_count', 'comments_count']

    def get_comments_count(self, obj):
        return obj.posts_comments.count()
