from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create token for the new user
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """
    Follow a user by adding them to the current user's following list.
    """
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Prevent users from following themselves
    if user_to_follow == request.user:
        return Response(
            {'error': 'You cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Add to following list
    request.user.following.add(user_to_follow)

    return Response(
        {'message': f'You are now following {user_to_follow.username}'},
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """
    Unfollow a user by removing them from the current user's following list.
    """
    try:
        user_to_unfollow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # Remove from following list
    request.user.following.remove(user_to_unfollow)

    return Response(
        {'message': f'You have unfollowed {user_to_unfollow.username}'},
        status=status.HTTP_200_OK
    )