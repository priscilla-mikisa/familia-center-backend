from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import CustomUser
from ..serializers.user_serializers import MinimalUserSerializer, FullUserSerializer

class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        
        # Filtering
        user_type = request.query_params.get('user_type')
        if user_type:
            users = users.filter(user_type=user_type)
            
        subscription_status = request.query_params.get('subscription_status')
        if subscription_status:
            users = users.filter(subscription_status=subscription_status)
            
        serializer = MinimalUserSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailView(APIView):
    def get(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = FullUserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        serializer = FullUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = get_object_or_404(CustomUser, id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CounselorListView(APIView):
    def get(self, request):
        counselors = CustomUser.objects.filter(user_type='counselor')
        serializer = MinimalUserSerializer(counselors, many=True)
        return Response(serializer.data)