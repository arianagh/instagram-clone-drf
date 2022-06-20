from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import PostsListView, ManageCommentView, AddCommentView,\
    ShowPostLikesComments, GetLikersView, LikeCreateView

router = DefaultRouter()
router.register("posts", PostsListView, basename="posts")

urlpatterns = [

    # path('posts-list/', PostsListView.as_view(), name="posts-list"),
    # path('posts-detail/<int:pk>', PostsDetailView.as_view(), name="posts-detail"),
    path('add-comment/<int:post_id>/<int:user_id>', AddCommentView.as_view(), name='add-comment'),
    path('manage-comment/<int:comment_id>', ManageCommentView.as_view(), name='manage-comment'),
    path('show-likes-comments/', ShowPostLikesComments.as_view(), name='show-likes-comments'),
    path('add-like/<int:post_id>', LikeCreateView.as_view(), name='add-like'),
    path('get-likers/<int:post_id>', GetLikersView.as_view(), name='get-likers'),

] + router.urls
