from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    """
    Return posts from users that the current user follows,
    ordered by creation date (most recent first).
    """
    # Get the current user
    user = request.user

    # Get all users that the current user is following
    following_users = user.following.all()

    # Get posts from followed users, ordered by creation date
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    # Serialize the posts
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)