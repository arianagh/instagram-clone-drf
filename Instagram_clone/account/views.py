from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import redirect
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, permissions, status, viewsets

from .models import Profile, FollowerTable, FollowerUser
from .serializers import RegisterSerializer, LoginSerializer, \
    ProfileSerializer, FollowerRequestSerializer, \
    FollowerListSerializer, FollowingListSerializer, \
    FollowerListNestedSerializer, FollowingListNestedSerializer


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        Token.objects.get_or_create(user=user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class Logout(APIView):

    def get(self, request):
        # logout(self.request.user)
        request.user.auth_token.delete()
        return redirect('login')


class RegisterUserAPIView(generics.CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserDetailAPIUpdate(RetrieveUpdateAPIView):
    """
    edit user profile
    """
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class Instagram(viewsets.ViewSet):
    """
    viewset to deal with everything about
    followers and followings functionality
    """
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user_follower_obj = FollowerTable.objects.get(user=request.user)
        qs = user_follower_obj.followers.all()
        serializer = FollowerListSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = FollowerRequestSerializer(data=request.data, context={'follower_request': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        else:
            return Response(serializer.errors)

    @action(methods=['POST'], detail=True, url_name='accept-follower', url_path='accept-follower')
    def accept_follower(self, request, pk):
        """
        give FollowerUser id to accept the request
        """
        following_obj = get_object_or_404(FollowerUser, pk=pk)
        # ke darkhaste ye user dge ro natone ghabol kne age khodesh nist
        if following_obj.following.user != request.user:
            return Response(status=403)
        following_obj.status = 'a'
        following_obj.save()
        return Response(status=200)

    @action(methods=['POST'], detail=True, url_name='delete-follower', url_path='delete-follower')
    def delete_follower(self, request, pk):
        following_obj = get_object_or_404(FollowerUser, pk=pk)
        if following_obj.following.user != request.user:
            return Response(status=403)
        following_obj.delete()
        return Response(status=204)

    @action(methods=['GET'], detail=False, url_name='following-list', url_path='following-list')
    def following_list(self, request):
        # harkasi ke request.user followeresh bashe ro miare pas mishe following haye on user
        qs = FollowerUser.objects.select_related("following").filter(follower=request.user, status="a")
        # user_obj = User.objects.get(id=request.user.id) # way 2 with reverse relation
        # qs = user_obj.followings.all()
        serializer = FollowingListSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=True, url_name='delete-following', url_path='delete-following')
    def delete_following(self, request, pk):
        following_obj = get_object_or_404(FollowerUser, pk=pk)
        if following_obj.follower != request.user:
            return Response(status=403)
        following_obj.delete()
        return Response(status=204)

    @action(methods=['GET'], detail=False, url_name='nested-followers', url_path='nested-followers')
    def nested_followers(self, request):
        qs = FollowerTable.objects.filter(user=request.user)
        serializer = FollowerListNestedSerializer(qs, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_name='nested-followings', url_path='nested-followings')
    def nested_followings(self, request):
        qs = User.objects.filter(id=request.user.id)
        serializer = FollowingListNestedSerializer(qs, many=True)
        return Response(serializer.data)


"""
help shell:
f = FollowerTable.objects.get(id=1) = arian
f = FollowerTable.objects.get(user=2) = arian
u = User.objects.get(id=5) 
t = FollowerUser.objects.filter(following=1) = followeraye arian
t = FollowerUser.objects.filter(follower=2) = followingaye arian
"""