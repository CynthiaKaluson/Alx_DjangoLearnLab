from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = CustomUser.objects.all().filter(id=user_id).first()
        if not user_to_follow:
            return Response({'error': 'User not found'}, status=404)

        request.user.following.add(user_to_follow)
        return Response({'message': 'User followed'}, status=200)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = CustomUser.objects.all().filter(id=user_id).first()
        if not user_to_unfollow:
            return Response({'error': 'User not found'}, status=404)

        request.user.following.remove(user_to_unfollow)
        return Response({'message': 'User unfollowed'}, status=200)
