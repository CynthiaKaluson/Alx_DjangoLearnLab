from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        users = CustomUser.objects.all()
        user_to_follow = get_object_or_404(users, id=user_id)

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)
        return Response(
            {"detail": "User followed successfully."},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        users = CustomUser.objects.all()
        user_to_unfollow = get_object_or_404(users, id=user_id)

        request.user.following.remove(user_to_unfollow)
        return Response(
            {"detail": "User unfollowed successfully."},
            status=status.HTTP_200_OK
        )
