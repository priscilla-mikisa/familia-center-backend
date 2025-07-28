from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from counselling_session.models import Session, Booking, Feedback
from ..serializers.session_serializers import (
    MinimalSessionSerializer, FullSessionSerializer, 
    BookingSerializer, FeedbackSerializer
)

class SessionListView(APIView):
    def get(self, request):
        sessions = Session.objects.filter(is_available=True)
        
        # Filtering
        session_type = request.query_params.get('type')
        if session_type:
            sessions = sessions.filter(session_type=session_type)
            
        program_id = request.query_params.get('program_id')
        if program_id:
            sessions = sessions.filter(program_id=program_id)
            
        counselor_id = request.query_params.get('counselor_id')
        if counselor_id:
            sessions = sessions.filter(counselor_id=counselor_id)
            
        # Upcoming sessions
        upcoming = request.query_params.get('upcoming')
        if upcoming:
            sessions = sessions.filter(scheduled_time__gte=timezone.now())
            
        serializer = MinimalSessionSerializer(sessions, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FullSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SessionDetailView(APIView):
    def get(self, request, id):
        session = get_object_or_404(Session, id=id)
        serializer = FullSessionSerializer(session)
        return Response(serializer.data)
    
    def put(self, request, id):
        session = get_object_or_404(Session, id=id)
        serializer = FullSessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        session = get_object_or_404(Session, id=id)
        session.is_available = False
        session.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookingView(APIView):
    def post(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        user = request.user
        
        # Check if already booked
        if Booking.objects.filter(user=user, session=session).exists():
            return Response(
                {"error": "User has already booked this session"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking = Booking.objects.create(user=user, session=session)
        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        user = request.user
        
        booking = get_object_or_404(Booking, user=user, session=session)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeedbackView(APIView):
    def post(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        user = request.user
        
        # Check if user attended the session
        booking = get_object_or_404(Booking, user=user, session=session)
        if not booking.attended:
            return Response(
                {"error": "User did not attend this session"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if feedback already provided
        if Feedback.objects.filter(user=user, session=session).exists():
            return Response(
                {"error": "Feedback already provided for this session"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, session=session)
            booking.feedback_provided = True
            booking.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)