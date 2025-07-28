from rest_framework import serializers
from counselling_session.models import Session, Booking, Feedback
from .user_serializers import MinimalUserSerializer, CounselorSerializer
from .program_serializers import MinimalProgramSerializer

class MinimalSessionSerializer(serializers.ModelSerializer):
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    
    class Meta:
        model = Session
        fields = [
            'id', 'title', 'session_type', 'session_type_display', 
            'scheduled_time', 'duration', 'is_available'
        ]

class FullSessionSerializer(serializers.ModelSerializer):
    counselor = CounselorSerializer()
    program = MinimalProgramSerializer()
    session_type_display = serializers.CharField(source='get_session_type_display', read_only=True)
    bookings = serializers.SerializerMethodField()
    
    def get_bookings(self, session):
        bookings = Booking.objects.filter(session=session)
        return BookingSerializer(bookings, many=True).data
    
    class Meta:
        model = Session
        fields = [
            'id', 'title', 'description', 'session_type', 'session_type_display',
            'program', 'counselor', 'scheduled_time', 'duration', 'google_meet_link',
            'recording_url', 'is_available', 'created_at', 'bookings'
        ]

class BookingSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer()
    session = MinimalSessionSerializer()
    
    class Meta:
        model = Booking
        fields = ['id', 'user', 'session', 'booked_at', 'attended', 'feedback_provided']

class FeedbackSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    session = MinimalSessionSerializer(read_only=True)
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'session', 'rating', 'rating_display', 'comment', 'created_at']