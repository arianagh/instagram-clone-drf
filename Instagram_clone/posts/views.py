from django.contrib.auth import get_user_model

from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, viewsets, status, authentication

from .models import Posts, Comment
from .permissions import IsOwnerOrPostOwnerOrReadOnly
from .serializers import PostListSerializer, PostDetailSerializer, \
    CommentSerializer, AuthorSerializer, ShowLikesCommentsSerializer

User = get_user_model()


class PostsListView(viewsets.ViewSet):
    """
    way 1 is with viewsets
    """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['GET'], detail=True, url_name='get-posts', url_path='get-posts')
    def get_posts(self, request, pk):
        """
        action to get posts list with the
        limitation of only followers and owner
        """
        follower_user = User.objects.get(id=request.user.id)
        user = get_object_or_404(User, pk=pk)
        query_follower = user.followers_table.followers.all()
        if query_follower.filter(follower=follower_user) or follower_user == user:
            queryset = Posts.objects.all().filter(creator=pk).order_by('-created_time')
            serializer = PostListSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response(status=403)

    def create(self, request):
        serializer = PostListSerializer(data=request.data, context={'creator': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def retrieve(self, request, pk=None):
        queryset = Posts.objects.filter(creator=request.user).all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostListSerializer(post)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        queryset = Posts.objects.filter(creator=request.user).all()
        post = get_object_or_404(queryset, pk=pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk=None):
        queryset = Posts.objects.all().filter(creator=self.request.user)
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostDetailSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentView(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id=None, user_id=None):
        follower_user = User.objects.get(id=request.user.id)
        user = get_object_or_404(User, id=user_id)
        query_follower = user.followers_table.followers.all()
        post = get_object_or_404(Posts, pk=post_id)
        if query_follower.filter(follower=follower_user) or follower_user == user:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(post=post, author=self.request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=403)


class ManageCommentView(RetrieveUpdateDestroyAPIView):
    """
    view to manage comments
    """
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = (IsOwnerOrPostOwnerOrReadOnly,)
    # authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class ShowPostLikesComments(ListAPIView):
    """
    view to get all likes and comments and posts for each owner posts
    """
    serializer_class = ShowLikesCommentsSerializer
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Posts.objects.all().filter(creator=self.request.user).order_by('-created_time')
        return queryset


class LikeCreateView(APIView):
    """ toggle like """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id=None):
        post = get_object_or_404(Posts, pk=post_id)
        user = self.request.user
        if user in post.likes.all():
            like = False
            post.likes.remove(user)
        else:
            like = True
            post.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)


class GetLikersView(ListAPIView):
    """ view to get all likes for each post """
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuthorSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Posts.objects.get(creator=self.request.user, pk=post_id).likes.all()
        return queryset


# class PostsListView(APIView):
#     """
#     way 2 is with api view and generics
#     """
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         qs = Posts.objects.all().filter(creator=request.user)
#         serializer = PostListSerializer(qs, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = PostListSerializer(data=request.data, context={'creator': request.user})
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)


# class PostsDetailView(RetrieveUpdateDestroyAPIView):
#
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#
#     queryset = Posts.objects.all()
#     serializer_class = PostDetailSerializer
#
#     def get_queryset(self):
#         return super().get_queryset().filter(creator=self.request.user)
#
