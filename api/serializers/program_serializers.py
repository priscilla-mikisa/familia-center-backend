from rest_framework import serializers
from programs.models import Program, ProgramEnrollment, Resource
from .user_serializers import MinimalUserSerializer, CounselorSerializer

class MinimalProgramSerializer(serializers.ModelSerializer):
    topic_display = serializers.CharField(source='get_topic_display', read_only=True)
    
    class Meta:
        model = Program
        fields = ['id', 'title', 'topic', 'topic_display', 'duration', 'is_active']

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'resource_type', 'file_url']

class FullProgramSerializer(serializers.ModelSerializer):
    counselor = CounselorSerializer()
    resources = ResourceSerializer(many=True, read_only=True)
    topic_display = serializers.CharField(source='get_topic_display', read_only=True)
    enrolled_users = serializers.SerializerMethodField()
    
    def get_enrolled_users(self, program):
        enrollments = ProgramEnrollment.objects.filter(program=program)
        return MinimalUserSerializer(
            [enrollment.user for enrollment in enrollments], 
            many=True
        ).data
    
    class Meta:
        model = Program
        fields = [
            'id', 'title', 'description', 'duration', 'topic', 'topic_display',
            'counselor', 'is_active', 'created_at', 'resources', 'enrolled_users'
        ]

class ProgramEnrollmentSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)
    program = MinimalProgramSerializer(read_only=True)
    
    class Meta:
        model = ProgramEnrollment
        fields = ['id', 'user', 'program', 'enrollment_date', 'progress', 'completed']