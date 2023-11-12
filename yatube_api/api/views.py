# from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)


@permission_classes([IsAuthenticated, IsAuthor])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@permission_classes([IsAuthenticated, IsAuthor])
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_id(self):
        print('*******************', self.kwargs)
        return get_object_or_404(Post, pk=self.kwargs.get('id'))

    def get_queryset(self):
        return Comment.objects.filter(post=self.get_id())

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_id())
