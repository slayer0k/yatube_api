from rest_framework.exceptions import ValidationError
from rest_framework import mixins, viewsets, filters, pagination
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from posts.models import Group, Follow, Post, User
from .serializers import (
    CommentSerializer, GroupSerializer, FollowSerializer, PostSerializer
)
from .permissions import AuthorOrReadOnly


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        if self.request.data.get('following') is None:
            raise ValidationError(
                'Отсутствует необходимое значение [following]'
            )
        following = get_object_or_404(
            User, username=self.request.data.get('following')
        )
        if self.request.user == following:
            raise ValidationError('нельзя подписаться на себя')
        if Follow.objects.filter(
            user=self.request.user,
            following=following
        ).exists():
            raise ValidationError('Подписка на этого автора уже есть')
        serializer.save(user=self.request.user, following=following)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'group')
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
