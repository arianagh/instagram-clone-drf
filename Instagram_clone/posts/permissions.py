from rest_framework import permissions


class IsOwnerOrPostOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission class which allow comment owner to do all http methods
    and Post Owner to DELETE comment"""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == 'DELETE' and \
                obj.post.creator.id == request.user.id:
            return True

        return obj.author.id == request.user.id
