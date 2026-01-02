from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification

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
        comment = serializer.save(author=self.request.user)

        # Create notification for post author
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def feed_view(request):
    """
    Return posts from users that the current user follows,
    ordered by creation date (most recent first).
    """
    user = request.user
    following_users = user.following.all()
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    """
    Like a post. Creates a Like object and generates a notification.
    """
    post = get_object_or_404(Post, pk=pk)

    # Use get_or_create to handle likes
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        return Response(
            {'detail': 'You have already liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create notification for post author
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )

    return Response(
        {'detail': 'Post liked successfully'},
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    """
    Unlike a post. Removes the Like object.
    """
    post = get_object_or_404(Post, pk=pk)

    try:
        like = Like.objects.get(user=request.user, post=post)
        like.delete()
        return Response(
            {'detail': 'Post unliked successfully'},
            status=status.HTTP_200_OK
        )
    except Like.DoesNotExist:
        return Response(
            {'detail': 'You have not liked this post'},
            status=status.HTTP_400_BAD_REQUEST
        )